from fastapi import APIRouter
import neurokit2 as nk
import numpy as np
import pandas as pd
from datetime import datetime
from firebase_admin import db
from apscheduler.schedulers.background import BackgroundScheduler

router = APIRouter(prefix="/hrv", tags=["HRV"])
raw_rr_intervals = []
scheduler = BackgroundScheduler()

WINDOW_SIZE = 300        # ~5 นาที (เหมาะกับ HRV frequency-domain)
OVERLAP_RATIO = 0.5      # overlap 50%

# -------------------- Firebase --------------------
def get_rr_interval_from_firebase():
    firebase_ref = db.reference("/Device/Inpatient/MD-V5-0000618/1s")
    input_data = firebase_ref.get()

    if not input_data:
        return None

    if "RR_Interval" in input_data:
        return float(input_data["RR_Interval"])

    if "HR" in input_data:
        hr = float(input_data["HR"])
        if hr > 0:
            return 60000 / hr  # BPM → ms

    return None


# -------------------- HRV Processing --------------------
def normalize_hrv_metric(metric_name, value):
    ranges = {
        "RMSSD": (10, 100),
        "SDNN": (20, 150),
        "pNN50": (0, 50),
        "MeanNN": (600, 1000),
        "LF": (100, 1500),
        "HF": (100, 1500),
        "LF_HF_Ratio": (0.5, 3.0)
    }

    if metric_name in ranges:
        min_val, max_val = ranges[metric_name]
        normalized = (value - min_val) / (max_val - min_val)
        return float(np.clip(normalized, 0, 1))

    return value


def preprocess_hrv(rr_intervals):
    rr_array = np.array(rr_intervals, dtype=float)

    if len(rr_array) < 30:
        print("HRV | RR intervals ไม่เพียงพอ")
        return None

    # Clean RR intervals (physiological range)
    rr_cleaned = rr_array[(rr_array >= 300) & (rr_array <= 2000)]

    if len(rr_cleaned) < 30:
        print("HRV | RR หลัง cleaning ไม่เพียงพอ")
        return None

    try:
        # Time-domain HRV
        hrv_time = nk.hrv_time(rr_cleaned, sampling_rate=None)

        hrv_metrics = {
            "RMSSD": hrv_time["HRV_RMSSD"].values[0],
            "SDNN": hrv_time["HRV_SDNN"].values[0],
            "pNN50": hrv_time["HRV_pNN50"].values[0],
            "MeanNN": hrv_time["HRV_MeanNN"].values[0],
        }

        # Frequency-domain HRV (ต้องมีข้อมูลมากพอ)
        if len(rr_cleaned) >= 120:
            hrv_freq = nk.hrv_frequency(rr_cleaned, method="welch")
            hrv_metrics.update({
                "LF": hrv_freq["HRV_LF"].values[0],
                "HF": hrv_freq["HRV_HF"].values[0],
                "LF_HF_Ratio": hrv_freq["HRV_LFHF"].values[0],
            })

        # Normalize
        normalized_metrics = {}
        for key, value in hrv_metrics.items():
            if value is not None and not np.isnan(value):
                normalized_metrics[key] = float(value)
                normalized_metrics[f"{key}_normalized"] = normalize_hrv_metric(key, value)

        return normalized_metrics

    except Exception as e:
        print(f"HRV | Error: {e}")
        return None

def store_processed_hrv_to_firebase(hrv_metrics):
    if not hrv_metrics:
        return

    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        **hrv_metrics
    }

    firebase_ref = db.reference("/Preprocessing/HRV")
    firebase_ref.push(data)

    print("--------------------------------------------------")
    print("HRV | Metrics")
    for k, v in hrv_metrics.items():
        print(f"{k}: {v:.4f}")
    print("--------------------------------------------------")


# -------------------- Main Loop --------------------
def collect_and_process_hrv():
    global raw_rr_intervals

    rr_value = get_rr_interval_from_firebase()
    if rr_value is None:
        return

    raw_rr_intervals.append(rr_value)

    if len(raw_rr_intervals) >= WINDOW_SIZE:
        hrv_metrics = preprocess_hrv(raw_rr_intervals)
        store_processed_hrv_to_firebase(hrv_metrics)

        overlap_size = int(WINDOW_SIZE * OVERLAP_RATIO)
        raw_rr_intervals = raw_rr_intervals[-overlap_size:]

def schedule_preprocessing_interval():
    if not scheduler.running:
        scheduler.add_job(
            collect_and_process_hrv,
            trigger="interval",
            seconds=1,
            max_instances=2,
            id="hrv_job",
            replace_existing=True
        )
        scheduler.start()


@router.post("/start_schedule_preprocessing_hrv")
async def start_schedule_preprocessing_hrv():
    try:
        schedule_preprocessing_interval()
        return {"message": "Started HRV preprocessing scheduler"}
    except Exception as e:
        return {"error": str(e)}


@router.get("/get_current_hrv")
async def get_current_hrv():
    try:
        firebase_ref = db.reference("/Preprocessing/HRV")
        hrv_data = firebase_ref.get()
        return hrv_data if hrv_data else {"message": "No HRV data available"}
    except Exception as e:
        return {"error": str(e)}
