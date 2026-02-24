# ModelOps Framework for Heart Disease Prediction with Automated Retraining

## Project Overview
A complete ModelOps framework built on top of a heart disease prediction ML model. 
The system automatically detects data drift, triggers retraining, evaluates the new 
model, and promotes it to production — all without human intervention.

---

## Architecture
```
Raw Data → Preprocessing → Model Training → MLflow Tracking
                                                    ↓
                                          Model Registry
                                          (Staging → Production)
                                                    ↓
                                          FastAPI REST Endpoint
                                                    ↓
                                          Evidently Monitoring
                                                    ↓
                                    [Drift Detected?] → Auto Retrain ↑
```

---

## Tech Stack

| Component | Tool |
|---|---|
| ML Model | Random Forest (scikit-learn) |
| Experiment Tracking | MLflow |
| Drift Detection | Evidently AI |
| API Serving | FastAPI |
| CI/CD | GitHub Actions |
| Language | Python 3.10 |

---

## Project Structure
```
heart-disease-prediction/
├── data/
│   ├── heart.csv              # Reference training data
│   └── current_data.csv       # Incoming production data
├── src/
│   ├── train.py               # MLflow-tracked training script
│   ├── drift_detector.py      # Evidently drift detection
│   └── retrain_pipeline.py    # Automated retraining loop
├── models/
│   ├── standard_scaler.pkl    # Saved StandardScaler
│   └── minmax_scaler.pkl      # Saved MinMaxScaler
├── reports/
│   └── drift_report.html      # Evidently drift report
├── notebooks/
│   ├── exploratory_data_analysis.ipynb
│   └── feature_engineering.ipynb
├── .github/
│   └── workflows/
│       └── retrain.yml        # GitHub Actions CI/CD
├── app.py                     # FastAPI serving endpoint
└── requirements.txt
```

---

## Dataset

- **Source:** Heart Disease Cleveland UCI Dataset
- **Size:** 1190 rows × 12 columns
- **Target:** Binary classification (0 = No Heart Disease, 1 = Heart Disease)
- **Features:** age, sex, chest pain type, resting bp, cholesterol, fasting blood sugar,
  resting ecg, max heart rate, exercise angina, oldpeak, ST slope

---

## Model Performance

| Metric | Score |
|---|---|
| Accuracy | 86.97% |
| ROC-AUC | 94.50% |
| F1 Score | 87.84% |

---

## How to Run

### 1. Clone the repo
```bash
git clone https://github.com/pujalameghana/heart-disease-prediction.git
cd heart-disease-prediction
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Train the model
```bash
python src/train.py
```

### 4. View MLflow UI
```bash
mlflow ui --port 5000
# Open: http://localhost:5000
```

### 5. Start FastAPI server
```bash
uvicorn app:app --reload --port 8000
# Open: http://localhost:8000/docs
```

### 6. Run drift detection
```bash
python src/drift_detector.py
```

### 7. Run full automated retraining pipeline
```bash
python src/retrain_pipeline.py
```

---

## API Usage

**Endpoint:** `POST /predict`

**Request:**
```json
{
  "age": 52,
  "sex": 1,
  "chest_pain_type": 0,
  "resting_bp_s": 125,
  "cholesterol": 212,
  "fasting_blood_sugar": 0,
  "resting_ecg": 1,
  "max_heart_rate": 168,
  "exercise_angina": 0,
  "oldpeak": 1.0,
  "st_slope": 2
}
```

**Response:**
```json
{
  "prediction": 0,
  "result": "No Heart Disease",
  "confidence": 0.4004,
  "risk_level": "Medium"
}
```

---

## Automated Retraining Pipeline

The pipeline runs automatically:
- **On every push** to master branch
- **Every Monday midnight** via scheduled cron job

### Pipeline Steps:
1. Check data drift using Evidently AI
2. If drift detected → trigger retraining
3. Evaluate new model accuracy
4. If accuracy > 85% → promote to Production
5. If accuracy < 85% → keep existing model

---

## Key Features

- **Experiment Tracking** — every training run logged with params and metrics
- **Model Versioning** — multiple model versions managed in MLflow registry
- **Drift Detection** — automatic detection when input data distribution shifts
- **Automated Retraining** — no human intervention needed
- **REST API** — real-time predictions via FastAPI
- **CI/CD** — automated pipeline runs on every code push

---

## Author
Pujala meghana  
Major Project — ModelOps Framework for Heart Disease Prediction