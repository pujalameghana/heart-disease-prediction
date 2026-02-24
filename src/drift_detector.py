# src/drift_detector.py
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from evidently.metrics import DatasetDriftMetric
import os

def check_drift(
    reference_path="data/heart.csv",
    current_path="data/current_data.csv",
    threshold=0.2
):
    # ── Load data ─────────────────────────────────────────────
    reference = pd.read_csv(reference_path)
    current   = pd.read_csv(current_path)

    print(f"Reference data shape : {reference.shape}")
    print(f"Current data shape   : {current.shape}")

    # ── Full visual drift report ───────────────────────────────
    os.makedirs("reports", exist_ok=True)
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference, current_data=current)
    report.save_html("reports/drift_report.html")
    print("✅ Drift report saved to reports/drift_report.html")

    # ── Programmatic drift check ───────────────────────────────
    drift_check = Report(metrics=[DatasetDriftMetric()])
    drift_check.run(reference_data=reference, current_data=current)
    result = drift_check.as_dict()

    drifted_columns = result["metrics"][0]["result"]["share_of_drifted_columns"]
    
    # ── Manual threshold check ────────────────────────────────
    drift_detected = drifted_columns >= threshold

    print(f"\n{'⚠️  DRIFT DETECTED' if drift_detected else '✅ No Drift Detected'}")
    print(f"Drifted columns : {drifted_columns:.0%}")
    print(f"Threshold used  : {threshold:.0%}")

    return drift_detected


if __name__ == "__main__":
    # ── Simulate drift by shifting age and cholesterol ────────
    print("Creating simulated current data with drift...")
    
    df = pd.read_csv("data/heart.csv")
    current = df.copy()
    
    # Artificially shift values to simulate drift
    current["age"]         = current["age"] + 20
    current["cholesterol"] = current["cholesterol"] + 80
    current["resting bp s"] = current["resting bp s"] + 30
    
    current.to_csv("data/current_data.csv", index=False)
    print("✅ current_data.csv created with simulated drift")

    # ── Run drift detection ───────────────────────────────────
    drift = check_drift()
    
    if drift:
        print("\n🔁 Drift detected — retraining should be triggered")
    else:
        print("\n✅ Model is stable — no retraining needed")