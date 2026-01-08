import joblib
import RandomForestClassifier as rf

model_dumb = joblib.load(rf"D:\Thermal_comfort\train_test_Model\2Class\Set6\rf_model.pkl")

#"D:\Work\Project\Model_Dumb\Model_Dumbxgb_model_['EDA_Phasic_EmotiBit', 'EDA_Tonic_EmotiBit', 'BMI', 'SkinTemp_Emo'].pkl"

if isinstance(model_dumb, rf.RandomForestClassifier):
    print("RandomForest model loaded successfully!")
else:
    raise ValueError("Loaded model is not an RandomForestClassifier. Please check the file path.")
