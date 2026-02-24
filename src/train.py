# src/train.py
# src/train.py
import pandas as pd
import numpy as np
import os
import pickle
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score

# ── MLflow setup ──────────────────────────────────────────────
_tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")
if not _tracking_uri.startswith("sqlite:///") and not _tracking_uri.startswith("http"):
    _tracking_uri = "sqlite:///mlflow.db"
mlflow.set_tracking_uri(_tracking_uri)
mlflow.set_experiment("heart-disease-prediction")




def preprocess(df):
    """Exact same preprocessing as feature_engineering notebook"""
    df = df.copy()

    # Encode categorical columns
    categorical_cols = ["sex", "chest pain type", "fasting blood sugar",
                        "resting ecg", "exercise angina", "ST slope"]
    
    le = LabelEncoder()
    for col in categorical_cols:
        if col in df.columns:
            df[col] = le.fit_transform(df[col].astype(str))

    # StandardScaler — same 4 columns as notebook
    standard_scaler = StandardScaler()
    df[["resting bp s", "cholesterol", "max heart rate", "age"]] = \
        standard_scaler.fit_transform(
            df[["resting bp s", "cholesterol", "max heart rate", "age"]]
        )

    # MinMaxScaler — oldpeak only
    min_max_scaler = MinMaxScaler()
    df[["oldpeak"]] = min_max_scaler.fit_transform(df[["oldpeak"]])

    return df, standard_scaler, min_max_scaler


def train_model(data_path="data/heart.csv"):
    # ── Load data ─────────────────────────────────────────────
    df = pd.read_csv(data_path)
    print(f"Dataset loaded: {df.shape}")

    # ── Preprocess ────────────────────────────────────────────
    df_processed, std_scaler, mm_scaler = preprocess(df)

    # ── Split features and target ─────────────────────────────
    X = df_processed.drop("target", axis=1)
    y = df_processed["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Train size: {X_train.shape} | Test size: {X_test.shape}")

    # ── MLflow run ────────────────────────────────────────────
    with mlflow.start_run():

        # Parameters
        params = {
            "n_estimators": 100,
            "max_depth": 5,
            "random_state": 42,
            "min_samples_split": 2
        }
        mlflow.log_params(params)

        # Train
        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)

        # Evaluate
        preds      = model.predict(X_test)
        proba      = model.predict_proba(X_test)[:, 1]

        accuracy   = accuracy_score(y_test, preds)
        auc        = roc_auc_score(y_test, proba)
        f1         = f1_score(y_test, preds)

        # Log metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("roc_auc",  auc)
        mlflow.log_metric("f1_score", f1)

        print(f"\n✅ Accuracy : {accuracy:.4f}")
        print(f"✅ ROC-AUC  : {auc:.4f}")
        print(f"✅ F1 Score : {f1:.4f}")

        # Log model to MLflow registry
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            registered_model_name="HeartDiseaseModel"
        )

        # Save scalers locally for FastAPI to use later
        os.makedirs("models", exist_ok=True)
        pickle.dump(std_scaler, open("models/standard_scaler.pkl", "wb"))
        pickle.dump(mm_scaler,  open("models/minmax_scaler.pkl",   "wb"))

        print("\n✅ Model registered in MLflow")
        print("✅ Scalers saved to models/")

        return model, accuracy


if __name__ == "__main__":
    train_model()