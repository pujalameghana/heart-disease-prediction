# app.py
import pandas as pd
import pickle
import mlflow.sklearn
from fastapi import FastAPI
from pydantic import BaseModel

# ── App setup ─────────────────────────────────────────────────
app = FastAPI(
    title="Heart Disease Prediction API",
    description="ModelOps Framework - Predicts heart disease from patient data",
    version="1.0.0"
)

# ── Load scalers ──────────────────────────────────────────────
std_scaler = pickle.load(open("models/standard_scaler.pkl", "rb"))
mm_scaler  = pickle.load(open("models/minmax_scaler.pkl",  "rb"))

# ── Load model from MLflow ────────────────────────────────────
model = mlflow.sklearn.load_model("models:/HeartDiseaseModel/1")

# ── Input schema ──────────────────────────────────────────────
class PatientData(BaseModel):
    age: float
    sex: int                  # 0 = Female, 1 = Male
    chest_pain_type: int      # 0-3
    resting_bp_s: float
    cholesterol: float
    fasting_blood_sugar: int  # 0 or 1
    resting_ecg: int          # 0-2
    max_heart_rate: float
    exercise_angina: int      # 0 or 1
    oldpeak: float
    st_slope: int             # 0-2

# ── Helper: preprocess input ──────────────────────────────────
def preprocess_input(data: PatientData):
    df = pd.DataFrame([{
        "age":                data.age,
        "sex":                data.sex,
        "chest pain type":    data.chest_pain_type,
        "resting bp s":       data.resting_bp_s,
        "cholesterol":        data.cholesterol,
        "fasting blood sugar":data.fasting_blood_sugar,
        "resting ecg":        data.resting_ecg,
        "max heart rate":     data.max_heart_rate,
        "exercise angina":    data.exercise_angina,
        "oldpeak":            data.oldpeak,
        "ST slope":           data.st_slope
    }])

    # Apply same scaling as training
    df[["resting bp s", "cholesterol", "max heart rate", "age"]] = \
        std_scaler.transform(df[["resting bp s", "cholesterol", "max heart rate", "age"]])
    
    df[["oldpeak"]] = mm_scaler.transform(df[["oldpeak"]])

    return df

# ── Routes ────────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "message": "Heart Disease Prediction API is running",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/predict")
def predict(patient: PatientData):
    df = preprocess_input(patient)
    
    prediction  = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    return {
        "prediction":  int(prediction),
        "result":      "Heart Disease Detected" if prediction == 1 else "No Heart Disease",
        "confidence":  round(float(probability), 4),
        "risk_level":  "High" if probability > 0.7 else "Medium" if probability > 0.4 else "Low"
    }