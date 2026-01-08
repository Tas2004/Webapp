def preprocess_hrv(hr_raw, normalize=True):
    hr_array = np.array(hr_raw, dtype=float)

    if len(hr_array) < 10:
        print("ข้อมูล HR ไม่พอสำหรับคำนวณ HRV")
        return None

    # 1. HR (bpm) → RR (ms)
    rr_intervals = 60000 / hr_array

    # 2. Remove outliers (physiological range)
    rr_intervals = rr_intervals[
        (rr_intervals > 300) & (rr_intervals < 2000)
    ]

    if len(rr_intervals) < 5:
        return None

    # 3. HRV time-domain features
    hrv_time = nk.hrv_time(rr_intervals, sampling_rate=1, show=False)

    hrv_features = {
        "RMSSD": float(hrv_time["HRV_RMSSD"].values[0]),
        "SDNN": float(hrv_time["HRV_SDNN"].values[0]),
        "MeanNN": float(hrv_time["HRV_MeanNN"].values[0]),
    }

    # 4. Z-score normalization (feature-level)
    if normalize:
        values = np.array(list(hrv_features.values()), dtype=float)
        mean = np.mean(values)
        std = np.std(values)

        if std == 0:
            norm_values = np.zeros_like(values)
        else:
            norm_values = (values - mean) / std

        hrv_features = dict(zip(
            ["RMSSD_Z", "SDNN_Z", "MeanNN_Z"],
            norm_values
        ))

    return hrv_features
