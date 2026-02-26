from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import numpy as np
import pandas as pd
import os
import glob

app = FastAPI(
    title="Heart Disease Prediction API",
    description="ModelOps Framework - Real-time Heart Disease Prediction",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_model():
    try:
        import mlflow.sklearn
        mlflow.set_tracking_uri("http://localhost:5000")
        model = mlflow.sklearn.load_model("models:/HeartDiseaseModel/1")
        return model
    except:
        pass
    try:
        pkl_files = glob.glob("mlruns/**/model.pkl", recursive=True)
        if pkl_files:
            return pickle.load(open(pkl_files[0], "rb"))
    except:
        pass
    return None

def load_scalers():
    try:
        std = pickle.load(open("models/standard_scaler.pkl", "rb"))
        mm  = pickle.load(open("models/minmax_scaler.pkl",  "rb"))
        return std, mm
    except:
        return None, None

model = load_model()
std_scaler, mm_scaler = load_scalers()

class PatientData(BaseModel):
    age: float
    sex: int
    chest_pain_type: int
    resting_bp: float
    cholesterol: float
    fasting_blood_sugar: int
    resting_ecg: int
    max_heart_rate: float
    exercise_angina: int
    oldpeak: float
    st_slope: int

@app.get("/")
def root():
    return {"message": "Heart Disease Prediction API", "status": "running", "model_loaded": model is not None}

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None, "scalers_loaded": std_scaler is not None}

@app.post("/predict")
def predict(patient: PatientData):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    input_df = pd.DataFrame([{
        "age": patient.age, "sex": patient.sex,
        "chest pain type": patient.chest_pain_type,
        "resting bp s": patient.resting_bp,
        "cholesterol": patient.cholesterol,
        "fasting blood sugar": patient.fasting_blood_sugar,
        "resting ecg": patient.resting_ecg,
        "max heart rate": patient.max_heart_rate,
        "exercise angina": patient.exercise_angina,
        "oldpeak": patient.oldpeak,
        "ST slope": patient.st_slope
    }])
    if std_scaler:
        input_df[["resting bp s","cholesterol","max heart rate","age"]] = \
            std_scaler.transform(input_df[["resting bp s","cholesterol","max heart rate","age"]])
    if mm_scaler:
        input_df[["oldpeak"]] = mm_scaler.transform(input_df[["oldpeak"]])
    prediction  = int(model.predict(input_df)[0])
    probability = float(model.predict_proba(input_df)[0][1])
    risk        = "High" if probability > 0.7 else "Medium" if probability > 0.4 else "Low"
    return {
        "prediction": prediction,
        "diagnosis": "Heart Disease Detected" if prediction==1 else "No Heart Disease",
        "probability": round(probability, 4),
        "risk_level": risk,
        "confidence": f"{probability*100:.1f}%" if prediction==1 else f"{(1-probability)*100:.1f}%"
    }

@app.get("/model/info")
def model_info():
    return {"model_type": type(model).__name__ if model else "Not loaded", "accuracy": "86.97%", "roc_auc": "94.50%", "f1_score": "87.84%"}
