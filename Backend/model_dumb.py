import joblib
import xgboost as xgb

model_dumb = joblib.load(rf"D:\Thermal_comfort\train_test_Model\2Class\Set6\rf_model.pkl")

#"D:\Work\Project\Model_Dumb\Model_Dumbxgb_model_['EDA_Phasic_EmotiBit', 'EDA_Tonic_EmotiBit', 'BMI', 'SkinTemp_Emo'].pkl"

if isinstance(model_dumb, xgb.XGBClassifier):
    print("XGBoost model loaded successfully!")
else:
    raise ValueError("Loaded model is not an XGBClassifier. Please check the file path.")
