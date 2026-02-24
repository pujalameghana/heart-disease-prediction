# src/retrain_pipeline.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from drift_detector import check_drift
from train import train_model
from mlflow.tracking import MlflowClient

# ── Config ────────────────────────────────────────────────────
ACCURACY_THRESHOLD = 0.85
MODEL_NAME         = "HeartDiseaseModel"

def get_current_production_accuracy():
    """Get accuracy of current production model from MLflow"""
    try:
        client  = MlflowClient()
        versions = client.get_latest_versions(MODEL_NAME, stages=["Production"])
        
        if not versions:
            print("No production model found — will register new one")
            return 0.0
        
        run_id   = versions[0].run_id
        accuracy = client.get_run(run_id).data.metrics.get("accuracy", 0.0)
        print(f"Current production accuracy: {accuracy:.4f}")
        return accuracy

    except Exception as e:
        print(f"Could not fetch production model: {e}")
        return 0.0


def promote_model(version):
    """Promote a model version to Production"""
    client = MlflowClient()
    client.transition_model_version_stage(
        name=MODEL_NAME,
        version=version,
        stage="Production"
    )
    print(f"✅ Model version {version} promoted to Production")


def run_pipeline():
    print("=" * 50)
    print("   MODELOPS RETRAINING PIPELINE STARTED")
    print("=" * 50)

    # ── Step 1: Check for drift ───────────────────────────────
    print("\n📊 Step 1: Checking for data drift...")
    drift = check_drift(
        reference_path="data/heart.csv",
        current_path="data/current_data.csv"
    )

    if not drift:
        print("\n✅ No drift detected — current model is stable")
        print("Pipeline complete — no retraining needed")
        return

    # ── Step 2: Retrain model ─────────────────────────────────
    print("\n🔁 Step 2: Drift detected — starting retraining...")
    _, new_accuracy = train_model(data_path="data/current_data.csv")

    # ── Step 3: Compare with threshold ───────────────────────
    print(f"\n📈 Step 3: Evaluating new model...")
    print(f"New model accuracy  : {new_accuracy:.4f}")
    print(f"Required threshold  : {ACCURACY_THRESHOLD}")

    if new_accuracy >= ACCURACY_THRESHOLD:
        # ── Step 4: Promote to production ────────────────────
        print(f"\n🚀 Step 4: New model meets threshold — promoting...")
        try:
            client   = MlflowClient()
            versions = client.get_latest_versions(MODEL_NAME, stages=["None"])
            if versions:
                latest_version = versions[-1].version
                promote_model(latest_version)
        except Exception as e:
            print(f"Promotion error: {e}")
    else:
        print(f"\n❌ New model accuracy {new_accuracy:.4f} below threshold {ACCURACY_THRESHOLD}")
        print("Keeping existing production model — retraining rejected")

    print("\n" + "=" * 50)
    print("   PIPELINE COMPLETE")
    print("=" * 50)


if __name__ == "__main__":
    run_pipeline()