# app_ui.py — Streamlit Dashboard for ModelOps Heart Disease Prediction
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import sys
import subprocess
from datetime import datetime

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Heart Disease ModelOps",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --red:    #E63946;
    --dark:   #0D1117;
    --card:   #161B22;
    --border: #30363D;
    --text:   #E6EDF3;
    --muted:  #8B949E;
    --green:  #3FB950;
    --yellow: #D29922;
    --blue:   #58A6FF;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--dark);
    color: var(--text);
}

.main { background-color: var(--dark); }
.block-container { padding: 2rem 2rem 2rem 2rem; }

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }

/* Header */
.hero {
    background: linear-gradient(135deg, #1a0a0a 0%, #0D1117 50%, #0a1a2a 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(230,57,70,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--text);
    margin: 0;
    letter-spacing: -0.5px;
}
.hero-title span { color: var(--red); }
.hero-sub {
    color: var(--muted);
    font-size: 0.9rem;
    margin-top: 0.4rem;
    font-weight: 300;
}

/* Metric cards */
.metric-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    text-align: center;
}
.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: var(--blue);
    margin: 0;
}
.metric-label {
    color: var(--muted);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.3rem;
}

/* Section headers */
.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 2px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.5rem;
    margin-bottom: 1.2rem;
}

/* Result cards */
.result-positive {
    background: linear-gradient(135deg, #1a0a0a, #200d0d);
    border: 1px solid var(--red);
    border-radius: 10px;
    padding: 1.5rem;
    text-align: center;
}
.result-negative {
    background: linear-gradient(135deg, #0a1a0a, #0d200d);
    border: 1px solid var(--green);
    border-radius: 10px;
    padding: 1.5rem;
    text-align: center;
}
.result-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.3rem;
    font-weight: 700;
    margin: 0.5rem 0;
}
.result-confidence {
    font-size: 0.85rem;
    color: var(--muted);
}

/* Status badges */
.badge-green {
    background: rgba(63,185,80,0.15);
    color: var(--green);
    border: 1px solid rgba(63,185,80,0.3);
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
    font-size: 0.75rem;
    font-family: 'Space Mono', monospace;
}
.badge-red {
    background: rgba(230,57,70,0.15);
    color: var(--red);
    border: 1px solid rgba(230,57,70,0.3);
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
    font-size: 0.75rem;
    font-family: 'Space Mono', monospace;
}
.badge-yellow {
    background: rgba(210,153,34,0.15);
    color: var(--yellow);
    border: 1px solid rgba(210,153,34,0.3);
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
    font-size: 0.75rem;
    font-family: 'Space Mono', monospace;
}

/* Pipeline steps */
.pipeline-step {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.step-number {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    min-width: 30px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: var(--card);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1rem;
}

/* Inputs */
.stSlider > div > div { background: var(--border) !important; }
.stSelectbox > div > div {
    background: var(--card) !important;
    border-color: var(--border) !important;
}

/* Buttons */
.stButton > button {
    background: var(--red) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
    padding: 0.6rem 1.5rem !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* Log box */
.log-box {
    background: #010409;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: var(--green);
    max-height: 300px;
    overflow-y: auto;
    white-space: pre-wrap;
}
</style>
""", unsafe_allow_html=True)

# ── Load model and scalers ────────────────────────────────────
@st.cache_resource
def load_artifacts():
    try:
        import mlflow.sklearn
        model      = mlflow.sklearn.load_model("models:/HeartDiseaseModel/1")
        std_scaler = pickle.load(open("models/standard_scaler.pkl", "rb"))
        mm_scaler  = pickle.load(open("models/minmax_scaler.pkl",  "rb"))
        return model, std_scaler, mm_scaler, True
    except Exception as e:
        # Fallback: load directly from mlruns pickle
        try:
            import glob
            pkl_files = glob.glob("mlruns/**/model.pkl", recursive=True)
            if pkl_files:
                model      = pickle.load(open(pkl_files[0], "rb"))
                std_scaler = pickle.load(open("models/standard_scaler.pkl", "rb"))
                mm_scaler  = pickle.load(open("models/minmax_scaler.pkl",  "rb"))
                return model, std_scaler, mm_scaler, True
        except:
            pass
        return None, None, None, False

model, std_scaler, mm_scaler, model_loaded = load_artifacts()

# ── Sidebar Navigation ────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='font-family: Space Mono, monospace; font-size: 1rem; 
         font-weight: 700; color: #E63946; margin-bottom: 1.5rem;'>
        🫀 MODELOPS
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["🏠 Dashboard", "🔬 Predict", "📊 Drift Detection", "🔁 Retrain Pipeline"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown(f"""
    <div style='font-size: 0.75rem; color: #8B949E;'>
        <div style='margin-bottom: 0.3rem;'>Model Status</div>
        <span class='{"badge-green" if model_loaded else "badge-red"}'>
            {"● LOADED" if model_loaded else "● NOT FOUND"}
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='font-size: 0.75rem; color: #8B949E; margin-top: 1rem;'>
        <div style='margin-bottom: 0.3rem;'>Last Updated</div>
        <span style='font-family: Space Mono, monospace; font-size: 0.7rem; color: #58A6FF;'>
            {datetime.now().strftime("%Y-%m-%d")}
        </span>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE 1: DASHBOARD
# ══════════════════════════════════════════════════════════════
if page == "🏠 Dashboard":

    st.markdown("""
    <div class='hero'>
        <p class='hero-title'>ModelOps Framework for <span>Heart Disease</span> Prediction</p>
        <p class='hero-sub'>Automated drift detection · Continuous retraining · Real-time prediction API</p>
    </div>
    """, unsafe_allow_html=True)

    # Metrics row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class='metric-card'>
            <p class='metric-value'>86.97%</p>
            <p class='metric-label'>Accuracy</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class='metric-card'>
            <p class='metric-value' style='color:#3FB950'>94.50%</p>
            <p class='metric-label'>ROC-AUC</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class='metric-card'>
            <p class='metric-value' style='color:#D29922'>87.84%</p>
            <p class='metric-label'>F1 Score</p>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class='metric-card'>
            <p class='metric-value' style='color:#E63946'>1190</p>
            <p class='metric-label'>Training Samples</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Pipeline + Tech Stack
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("<p class='section-header'>Automated Pipeline</p>", unsafe_allow_html=True)
        steps = [
            ("01", "🟢", "Data Ingestion", "Load reference & current patient data"),
            ("02", "🟢", "Drift Detection", "Evidently AI checks distribution shift"),
            ("03", "🟢", "Auto Retraining", "Model retrained on new data if drift > 20%"),
            ("04", "🟢", "Evaluation", "New model accuracy compared to threshold"),
            ("05", "🟢", "Promotion", "Best model promoted to Production in MLflow"),
            ("06", "🟢", "API Serving", "FastAPI serves predictions in real-time"),
        ]
        for num, icon, title, desc in steps:
            st.markdown(f"""
            <div class='pipeline-step'>
                <span class='step-number'>{num}</span>
                <span style='font-size:1rem'>{icon}</span>
                <div>
                    <div style='font-weight:600; font-size:0.9rem'>{title}</div>
                    <div style='color:#8B949E; font-size:0.78rem'>{desc}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("<p class='section-header'>Tech Stack</p>", unsafe_allow_html=True)
        stack = [
            ("🤖", "Random Forest", "ML Model"),
            ("📊", "MLflow", "Experiment Tracking"),
            ("🔍", "Evidently AI", "Drift Detection"),
            ("⚡", "FastAPI", "Model Serving"),
            ("🔄", "GitHub Actions", "CI/CD Pipeline"),
            ("🎯", "Streamlit", "Dashboard UI"),
        ]
        for icon, name, role in stack:
            st.markdown(f"""
            <div style='background:#161B22; border:1px solid #30363D; border-radius:8px;
                        padding:0.7rem 1rem; margin-bottom:0.4rem; display:flex;
                        align-items:center; gap:0.8rem;'>
                <span style='font-size:1.2rem'>{icon}</span>
                <div>
                    <div style='font-weight:600; font-size:0.85rem'>{name}</div>
                    <div style='color:#8B949E; font-size:0.75rem'>{role}</div>
                </div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE 2: PREDICT
# ══════════════════════════════════════════════════════════════
elif page == "🔬 Predict":

    st.markdown("""
    <div class='hero'>
        <p class='hero-title'>Patient <span>Risk</span> Assessment</p>
        <p class='hero-sub'>Enter patient vitals to get an instant heart disease prediction</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("<p class='section-header'>Patient Information</p>", unsafe_allow_html=True)

        r1c1, r1c2, r1c3 = st.columns(3)
        with r1c1:
            age = st.slider("Age", 20, 90, 52)
        with r1c2:
            sex = st.selectbox("Sex", [0, 1], format_func=lambda x: "Female" if x == 0 else "Male")
        with r1c3:
            chest_pain = st.selectbox("Chest Pain Type", [0, 1, 2, 3],
                format_func=lambda x: ["Typical Angina", "Atypical Angina",
                                       "Non-Anginal", "Asymptomatic"][x])

        r2c1, r2c2, r2c3 = st.columns(3)
        with r2c1:
            resting_bp = st.slider("Resting BP (mmHg)", 80, 200, 125)
        with r2c2:
            cholesterol = st.slider("Cholesterol (mg/dl)", 100, 600, 212)
        with r2c3:
            fasting_bs = st.selectbox("Fasting Blood Sugar > 120", [0, 1],
                format_func=lambda x: "No" if x == 0 else "Yes")

        r3c1, r3c2, r3c3 = st.columns(3)
        with r3c1:
            resting_ecg = st.selectbox("Resting ECG", [0, 1, 2],
                format_func=lambda x: ["Normal", "ST-T Abnormality", "LV Hypertrophy"][x])
        with r3c2:
            max_hr = st.slider("Max Heart Rate", 60, 220, 168)
        with r3c3:
            exercise_angina = st.selectbox("Exercise Angina", [0, 1],
                format_func=lambda x: "No" if x == 0 else "Yes")

        r4c1, r4c2 = st.columns(2)
        with r4c1:
            oldpeak = st.slider("Oldpeak (ST Depression)", 0.0, 6.0, 1.0, 0.1)
        with r4c2:
            st_slope = st.selectbox("ST Slope", [0, 1, 2],
                format_func=lambda x: ["Upsloping", "Flat", "Downsloping"][x])

        predict_btn = st.button("🫀 Analyze Patient Risk")

    with col2:
        st.markdown("<p class='section-header'>Result</p>", unsafe_allow_html=True)

        if predict_btn:
            if not model_loaded:
                st.error("Model not loaded. Please train the model first.")
            else:
                # Preprocess
                input_df = pd.DataFrame([{
                    "age": age,
                    "sex": sex,
                    "chest pain type": chest_pain,
                    "resting bp s": resting_bp,
                    "cholesterol": cholesterol,
                    "fasting blood sugar": fasting_bs,
                    "resting ecg": resting_ecg,
                    "max heart rate": max_hr,
                    "exercise angina": exercise_angina,
                    "oldpeak": oldpeak,
                    "ST slope": st_slope
                }])

                input_df[["resting bp s", "cholesterol", "max heart rate", "age"]] = \
                    std_scaler.transform(input_df[["resting bp s", "cholesterol",
                                                   "max heart rate", "age"]])
                input_df[["oldpeak"]] = mm_scaler.transform(input_df[["oldpeak"]])

                pred  = model.predict(input_df)[0]
                prob  = model.predict_proba(input_df)[0][1]
                risk  = "High" if prob > 0.7 else "Medium" if prob > 0.4 else "Low"
                rcolor = {"High": "#E63946", "Medium": "#D29922", "Low": "#3FB950"}[risk]

                if pred == 1:
                    st.markdown(f"""
                    <div class='result-positive'>
                        <div style='font-size:2.5rem'>⚠️</div>
                        <p class='result-title' style='color:#E63946'>Heart Disease<br>Detected</p>
                        <p class='result-confidence'>Confidence: {prob:.1%}</p>
                        <p style='color:{rcolor}; font-weight:600; margin-top:0.5rem'>
                            {risk} Risk
                        </p>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='result-negative'>
                        <div style='font-size:2.5rem'>✅</div>
                        <p class='result-title' style='color:#3FB950'>No Heart Disease<br>Detected</p>
                        <p class='result-confidence'>Confidence: {1-prob:.1%}</p>
                        <p style='color:{rcolor}; font-weight:600; margin-top:0.5rem'>
                            {risk} Risk
                        </p>
                    </div>""", unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style='background:#161B22; border:1px solid #30363D; border-radius:8px; padding:1rem;'>
                    <p style='font-family: Space Mono, monospace; font-size:0.7rem; color:#8B949E; margin:0 0 0.5rem 0;'>
                        PREDICTION DETAILS
                    </p>
                    <div style='font-size:0.82rem; line-height:1.8'>
                        <div>Prediction: <b style='color:#58A6FF'>{pred}</b></div>
                        <div>Probability: <b style='color:#58A6FF'>{prob:.4f}</b></div>
                        <div>Risk Level: <b style='color:{rcolor}'>{risk}</b></div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background:#161B22; border:1px dashed #30363D; border-radius:10px;
                        padding:3rem 1rem; text-align:center; color:#8B949E;'>
                <div style='font-size:2rem; margin-bottom:1rem'>🫀</div>
                <div style='font-size:0.85rem'>Fill in patient details<br>and click Analyze</div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE 3: DRIFT DETECTION
# ══════════════════════════════════════════════════════════════
elif page == "📊 Drift Detection":

    st.markdown("""
    <div class='hero'>
        <p class='hero-title'>Data <span>Drift</span> Monitoring</p>
        <p class='hero-sub'>Detect when incoming patient data deviates from training distribution</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("<p class='section-header'>Run Drift Detection</p>", unsafe_allow_html=True)

        st.markdown("""
        <div style='background:#161B22; border:1px solid #30363D; border-radius:8px;
                    padding:1.2rem; margin-bottom:1rem; font-size:0.85rem; line-height:1.7;'>
            <b>How it works:</b><br>
            1. Compares reference data (training) with current incoming data<br>
            2. Uses Evidently AI statistical tests per column<br>
            3. Flags drift if >20% of columns show significant shift<br>
            4. Generates a full visual HTML report
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔍 Run Drift Detection Now"):
            with st.spinner("Running Evidently drift analysis..."):
                try:
                    result = subprocess.run(
                        [sys.executable, "src/drift_detector.py"],
                        capture_output=True, text=True, timeout=60
                    )
                    output = result.stdout + result.stderr

                    st.markdown(f"""
                    <div class='log-box'>{output}</div>
                    """, unsafe_allow_html=True)

                    if "DRIFT DETECTED" in output:
                        st.markdown("""
                        <div style='background:rgba(230,57,70,0.1); border:1px solid #E63946;
                                    border-radius:8px; padding:1rem; margin-top:1rem; text-align:center;'>
                            <b style='color:#E63946'>⚠️ Drift Detected — Retraining Recommended</b>
                        </div>""", unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div style='background:rgba(63,185,80,0.1); border:1px solid #3FB950;
                                    border-radius:8px; padding:1rem; margin-top:1rem; text-align:center;'>
                            <b style='color:#3FB950'>✅ No Drift — Model is Stable</b>
                        </div>""", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Error: {e}")

    with col2:
        st.markdown("<p class='section-header'>Drift Report</p>", unsafe_allow_html=True)

        if os.path.exists("reports/drift_report.html"):
            with open("reports/drift_report.html", "r") as f:
                html_content = f.read()
            st.components.v1.html(html_content, height=500, scrolling=True)
        else:
            st.markdown("""
            <div style='background:#161B22; border:1px dashed #30363D; border-radius:10px;
                        padding:3rem 1rem; text-align:center; color:#8B949E;'>
                <div style='font-size:2rem; margin-bottom:1rem'>📊</div>
                <div style='font-size:0.85rem'>Run drift detection to<br>generate the report</div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE 4: RETRAIN PIPELINE
# ══════════════════════════════════════════════════════════════
elif page == "🔁 Retrain Pipeline":

    st.markdown("""
    <div class='hero'>
        <p class='hero-title'>Automated <span>Retraining</span> Pipeline</p>
        <p class='hero-sub'>Trigger full ModelOps loop — drift check, retrain, evaluate, promote</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("<p class='section-header'>Pipeline Steps</p>", unsafe_allow_html=True)

        steps = [
            ("01", "Check data drift with Evidently AI"),
            ("02", "If drift > 20% → trigger retraining"),
            ("03", "Train new Random Forest model"),
            ("04", "Log run to MLflow experiment tracker"),
            ("05", "Compare accuracy against 85% threshold"),
            ("06", "Promote to Production if threshold met"),
        ]
        for num, desc in steps:
            st.markdown(f"""
            <div class='pipeline-step'>
                <span class='step-number'>{num}</span>
                <span style='font-size:0.85rem'>{desc}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚀 Run Full Retraining Pipeline"):
            with st.spinner("Running automated retraining pipeline..."):
                try:
                    result = subprocess.run(
                        [sys.executable, "src/retrain_pipeline.py"],
                        capture_output=True, text=True, timeout=120
                    )
                    output = result.stdout + result.stderr
                    st.session_state["pipeline_output"] = output
                except Exception as e:
                    st.session_state["pipeline_output"] = f"Error: {e}"

    with col2:
        st.markdown("<p class='section-header'>Pipeline Output</p>", unsafe_allow_html=True)

        if "pipeline_output" in st.session_state:
            output = st.session_state["pipeline_output"]
            st.markdown(f"""
            <div class='log-box'>{output}</div>
            """, unsafe_allow_html=True)

            if "PIPELINE COMPLETE" in output:
                st.markdown("""
                <div style='background:rgba(63,185,80,0.1); border:1px solid #3FB950;
                            border-radius:8px; padding:1rem; margin-top:1rem; text-align:center;'>
                    <b style='color:#3FB950'>✅ Pipeline Completed Successfully</b><br>
                    <span style='font-size:0.8rem; color:#8B949E'>
                        Check MLflow UI for the new model version
                    </span>
                </div>""", unsafe_allow_html=True)
            elif "Error" in output or "Traceback" in output:
                st.markdown("""
                <div style='background:rgba(230,57,70,0.1); border:1px solid #E63946;
                            border-radius:8px; padding:1rem; margin-top:1rem; text-align:center;'>
                    <b style='color:#E63946'>❌ Pipeline encountered an error</b>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background:#161B22; border:1px dashed #30363D; border-radius:10px;
                        padding:3rem 1rem; text-align:center; color:#8B949E;'>
                <div style='font-size:2rem; margin-bottom:1rem'>🔁</div>
                <div style='font-size:0.85rem'>Click the button to run<br>the full pipeline</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background:#161B22; border:1px solid #30363D; border-radius:8px; padding:1rem;'>
            <p style='font-family: Space Mono, monospace; font-size:0.7rem; 
                      color:#8B949E; margin:0 0 0.5rem 0;'>AUTO-TRIGGER CONDITIONS</p>
            <div style='font-size:0.82rem; line-height:1.8; color:#E6EDF3;'>
                <div>📅 Every Monday at midnight (cron)</div>
                <div>🔀 Every push to master branch</div>
                <div>📊 When drift exceeds 20% threshold</div>
            </div>
        </div>""", unsafe_allow_html=True)