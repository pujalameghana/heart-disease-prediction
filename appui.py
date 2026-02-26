import streamlit as st
st.set_page_config(page_title="Heart Disease ModelOps", page_icon="🫀", layout="wide", initial_sidebar_state="collapsed")

import pandas as pd
import numpy as np
import pickle
import os
import sys
import subprocess
import json
from datetime import datetime

USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def check_password(username, password):
    users = load_users()
    if username not in users:
        return False
    return users[username]["password"] == password

def register_user(username, name, password):
    users = load_users()
    if username in users:
        return False, "Username already exists"
    users[username] = {"name": name, "password": password}
    save_users(users)
    return True, "Account created successfully"

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.markdown("""
    <style>
    #MainMenu, footer, header { visibility: hidden; }
    .stButton > button {
        background: #E63946 !important; color: white !important;
        border: none !important; border-radius: 8px !important;
        width: 100% !important; padding: 0.6rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background:#161B22;border:1px solid #30363D;border-radius:14px;
                    padding:2rem;text-align:center;margin-bottom:1rem;'>
            <div style='font-size:3rem'>🫀</div>
            <p style='font-size:1.1rem;font-weight:700;color:#E6EDF3;margin:0;'>Heart Disease ModelOps</p>
            <p style='color:#8B949E;font-size:0.8rem;margin-top:0.3rem;margin-bottom:0;'>ModelOps Framework Dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔐 Sign In", "📝 Sign Up"])
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            login_user = st.text_input("Username", key="login_user", placeholder="Enter username")
            login_pass = st.text_input("Password", type="password", key="login_pass", placeholder="Enter password")
            if st.button("🔐 Sign In", key="signin_btn"):
                u, p = login_user.strip(), login_pass.strip()
                if not u or not p:
                    st.error("Please enter both fields")
                elif check_password(u, p):
                    users = load_users()
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = u
                    st.session_state["name"] = users[u]["name"]
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
            st.markdown("<div style='margin-top:1rem;font-size:0.75rem;color:#8B949E;text-align:center;'>Default: <b style='color:#58A6FF'>doctor</b> / doctor123 &nbsp;|&nbsp; <b style='color:#58A6FF'>panel</b> / panel123</div>", unsafe_allow_html=True)
        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            reg_name    = st.text_input("Full Name", key="reg_name", placeholder="Your full name")
            reg_user    = st.text_input("Username", key="reg_user", placeholder="Choose username")
            reg_pass    = st.text_input("Password", type="password", key="reg_pass", placeholder="Choose password")
            reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Confirm password")
            if st.button("📝 Create Account", key="signup_btn"):
                n, u, p, cp = reg_name.strip(), reg_user.strip(), reg_pass.strip(), reg_confirm.strip()
                if not all([n, u, p, cp]):
                    st.error("Please fill in all fields")
                elif p != cp:
                    st.error("❌ Passwords do not match")
                else:
                    success, message = register_user(u, n, p)
                    st.success("✅ Account created! Go to Sign In.") if success else st.error(f"❌ {message}")
    st.stop()

# ── CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.block-container { padding: 1rem 2rem 2rem 2rem !important; }
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { display: none !important; }

.top-nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.8rem 1.5rem; margin-bottom: 1.5rem;
    background: rgba(128,128,128,0.05);
    border: 1px solid rgba(128,128,128,0.15);
    border-radius: 12px;
}
.nav-brand { font-family:'Space Mono',monospace; font-size:1rem; font-weight:700; color:#E63946; }
.nav-links { display:flex; gap:0.5rem; }
.nav-user { font-size:0.78rem; opacity:0.7; }

.hero { border:1px solid rgba(128,128,128,0.2);border-radius:12px;padding:2rem 2.5rem;
        margin-bottom:2rem;background:linear-gradient(135deg,rgba(230,57,70,0.05) 0%,transparent 50%,rgba(88,166,255,0.05) 100%); }
.hero-title { font-family:'Space Mono',monospace;font-size:1.6rem;font-weight:700;margin:0; }
.hero-title span { color:#E63946; }
.hero-sub { font-size:0.9rem;margin-top:0.4rem;opacity:0.7; }

.metric-card { border:1px solid rgba(128,128,128,0.2);border-radius:10px;padding:1.2rem 1.5rem;
               text-align:center;background:rgba(128,128,128,0.05); }
.metric-value { font-family:'Space Mono',monospace;font-size:2rem;font-weight:700;margin:0; }
.metric-label { font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;margin-top:0.3rem;opacity:0.7; }

.section-header { font-family:'Space Mono',monospace;font-size:0.8rem;text-transform:uppercase;
                  letter-spacing:2px;border-bottom:1px solid rgba(128,128,128,0.2);
                  padding-bottom:0.5rem;margin-bottom:1.2rem;opacity:0.7; }
.pipeline-step { border:1px solid rgba(128,128,128,0.2);border-radius:8px;padding:1rem 1.2rem;
                 margin-bottom:0.5rem;display:flex;align-items:center;gap:1rem;background:rgba(128,128,128,0.03); }
.step-number { font-family:'Space Mono',monospace;font-size:0.7rem;opacity:0.5;min-width:30px; }
.result-positive { border:2px solid #E63946;border-radius:10px;padding:1.5rem;text-align:center;background:rgba(230,57,70,0.08); }
.result-negative { border:2px solid #3FB950;border-radius:10px;padding:1.5rem;text-align:center;background:rgba(63,185,80,0.08); }
.result-title { font-family:'Space Mono',monospace;font-size:1.3rem;font-weight:700;margin:0.5rem 0; }
.log-box { background:#010409;border:1px solid #30363D;border-radius:8px;padding:1rem;
           font-family:'Space Mono',monospace;font-size:0.75rem;color:#3FB950;
           max-height:300px;overflow-y:auto;white-space:pre-wrap; }
.stButton > button {
    background: rgba(128,128,128,0.08) !important;
    color: inherit !important;
    border: 1px solid rgba(128,128,128,0.2) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 0.45rem 0.5rem !important;
    width: 100% !important;
    height: 2.6rem !important;
    white-space: nowrap !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    background: rgba(230,57,70,0.15) !important;
    border-color: #E63946 !important;
    color: #E63946 !important;
}
/* Active page button */
.stButton > button[kind="primary"] {
    background: #E63946 !important;
    color: white !important;
    border-color: #E63946 !important;
}
/* Login/action buttons specifically */
div[data-testid="column"] .stButton > button#signin_btn,
div[data-testid="column"] .stButton > button#signup_btn,
div[data-testid="column"] .stButton > button#logout_btn {
    background: #E63946 !important;
    color: white !important;
    border: none !important;
}
div[data-testid="stTabs"] button { font-family:'Space Mono',monospace !important; font-size:0.8rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Load model ────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    try:
        import mlflow.sklearn
        model = mlflow.sklearn.load_model("models:/HeartDiseaseModel/1")
        std_scaler = pickle.load(open("models/standard_scaler.pkl","rb"))
        mm_scaler  = pickle.load(open("models/minmax_scaler.pkl","rb"))
        return model, std_scaler, mm_scaler, True
    except:
        try:
            import glob
            pkl_files = glob.glob("mlruns/**/model.pkl", recursive=True)
            if pkl_files:
                model = pickle.load(open(pkl_files[0],"rb"))
                std_scaler = pickle.load(open("models/standard_scaler.pkl","rb"))
                mm_scaler  = pickle.load(open("models/minmax_scaler.pkl","rb"))
                return model, std_scaler, mm_scaler, True
        except:
            pass
    return None, None, None, False

model, std_scaler, mm_scaler, model_loaded = load_artifacts()
status_color = "#3FB950" if model_loaded else "#E63946"
status_text  = "● LOADED" if model_loaded else "● NOT FOUND"

# ── TOP NAV ───────────────────────────────────────────────────
name = st.session_state.get("name", "")
if "page" not in st.session_state:
    st.session_state["page"] = "🏠 Dashboard"

pages = ["🏠 Dashboard", "🔬 Predict", "📊 Drift Detection", "🔁 Retrain Pipeline"]

# CSS to highlight active nav button
active_page = st.session_state["page"]
active_css = ""
for i, p in enumerate(pages):
    if p == active_page:
        active_css += f"""
        div[data-testid="column"]:nth-child({i+2}) .stButton > button {{
            background: #E63946 !important;
            color: white !important;
            border-color: #E63946 !important;
        }}"""
st.markdown(f"<style>{active_css}</style>", unsafe_allow_html=True)

col_brand, c1, c2, c3, c4, col_user = st.columns([1.2, 1, 1, 1, 1, 1.5])
with col_brand:
    st.markdown("<div style='font-family:Space Mono,monospace;font-size:0.95rem;font-weight:700;color:#E63946;padding-top:0.55rem;'>🫀 MODELOPS</div>", unsafe_allow_html=True)

nav_cols = [c1, c2, c3, c4]
for i, p in enumerate(pages):
    with nav_cols[i]:
        if st.button(p, key=f"nav_{i}"):
            st.session_state["page"] = p
            st.rerun()

with col_user:
    st.markdown(f"""
    <div style='text-align:right;padding-top:0.2rem;'>
        <div style='font-size:0.75rem;opacity:0.8;'>👤 <b>{name}</b></div>
        <div style='font-size:0.68rem;color:{status_color};font-family:Space Mono,monospace;'>{status_text}</div>
    </div>""", unsafe_allow_html=True)
    if st.button("🚪 Logout", key="logout_btn"):
        st.session_state["logged_in"] = False
        st.rerun()

st.markdown("<hr style='border:none;border-top:1px solid rgba(128,128,128,0.15);margin:0 0 1.5rem 0;'>", unsafe_allow_html=True)

page = st.session_state.get("page", "🏠 Dashboard")

# ══════════════════════════════════════════════════════════════
# PAGE 1: DASHBOARD
# ══════════════════════════════════════════════════════════════
if page == "🏠 Dashboard":
    st.markdown("<div class='hero'><p class='hero-title'>ModelOps Framework for <span>Heart Disease</span> Prediction</p><p class='hero-sub'>Automated drift detection · Continuous retraining · Real-time prediction API</p></div>", unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown("<div class='metric-card'><p class='metric-value' style='color:#58A6FF'>86.97%</p><p class='metric-label'>Accuracy</p></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='metric-card'><p class='metric-value' style='color:#3FB950'>94.50%</p><p class='metric-label'>ROC-AUC</p></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='metric-card'><p class='metric-value' style='color:#D29922'>87.84%</p><p class='metric-label'>F1 Score</p></div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='metric-card'><p class='metric-value' style='color:#E63946'>1190</p><p class='metric-label'>Training Samples</p></div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([3,2])
    with col1:
        st.markdown("<p class='section-header'>Automated Pipeline</p>", unsafe_allow_html=True)
        for num,icon,title,desc in [
            ("01","🟢","Data Ingestion","Load reference & current patient data"),
            ("02","🟢","Drift Detection","Evidently AI checks distribution shift"),
            ("03","🟢","Auto Retraining","Model retrained on new data if drift > 20%"),
            ("04","🟢","Evaluation","New model accuracy compared to threshold"),
            ("05","🟢","Promotion","Best model promoted to Production in MLflow"),
            ("06","🟢","API Serving","FastAPI serves predictions in real-time"),
        ]:
            st.markdown(f"<div class='pipeline-step'><span class='step-number'>{num}</span><span style='font-size:1rem'>{icon}</span><div><div style='font-weight:600;font-size:0.9rem'>{title}</div><div style='font-size:0.78rem;opacity:0.7'>{desc}</div></div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<p class='section-header'>Tech Stack</p>", unsafe_allow_html=True)
        for icon,name_,role in [("🤖","Random Forest","ML Model"),("📊","MLflow","Experiment Tracking"),("🔍","Evidently AI","Drift Detection"),("⚡","FastAPI","Model Serving"),("🔄","GitHub Actions","CI/CD Pipeline"),("🎯","Streamlit","Dashboard UI")]:
            st.markdown(f"<div style='border:1px solid rgba(128,128,128,0.2);border-radius:8px;padding:0.7rem 1rem;margin-bottom:0.4rem;display:flex;align-items:center;gap:0.8rem;background:rgba(128,128,128,0.03);'><span style='font-size:1.2rem'>{icon}</span><div><div style='font-weight:600;font-size:0.85rem'>{name_}</div><div style='font-size:0.75rem;opacity:0.7'>{role}</div></div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE 2: PREDICT
# ══════════════════════════════════════════════════════════════
elif page == "🔬 Predict":
    st.markdown("<div class='hero'><p class='hero-title'>Patient <span>Risk</span> Assessment</p><p class='hero-sub'>Enter patient vitals to get an instant heart disease prediction</p></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("<p class='section-header'>Patient Information</p>", unsafe_allow_html=True)
        r1c1,r1c2,r1c3 = st.columns(3)
        with r1c1: age = st.slider("Age",20,90,52)
        with r1c2: sex = st.selectbox("Sex",[0,1],format_func=lambda x:"Female" if x==0 else "Male")
        with r1c3: chest_pain = st.selectbox("Chest Pain",[0,1,2,3],format_func=lambda x:["Typical","Atypical","Non-Anginal","Asymptomatic"][x])
        r2c1,r2c2,r2c3 = st.columns(3)
        with r2c1: resting_bp = st.slider("Resting BP",80,200,125)
        with r2c2: cholesterol = st.slider("Cholesterol",100,600,212)
        with r2c3: fasting_bs = st.selectbox("Fasting BS>120",[0,1],format_func=lambda x:"No" if x==0 else "Yes")
        r3c1,r3c2,r3c3 = st.columns(3)
        with r3c1: resting_ecg = st.selectbox("Resting ECG",[0,1,2],format_func=lambda x:["Normal","ST-T Abnorm","LV Hypertrophy"][x])
        with r3c2: max_hr = st.slider("Max HR",60,220,168)
        with r3c3: exercise_angina = st.selectbox("Exercise Angina",[0,1],format_func=lambda x:"No" if x==0 else "Yes")
        r4c1,r4c2 = st.columns(2)
        with r4c1: oldpeak = st.slider("Oldpeak",0.0,6.0,1.0,0.1)
        with r4c2: st_slope = st.selectbox("ST Slope",[0,1,2],format_func=lambda x:["Upsloping","Flat","Downsloping"][x])
        predict_btn = st.button("🫀 Analyze Patient Risk")
    with col2:
        st.markdown("<p class='section-header'>Result</p>", unsafe_allow_html=True)
        if predict_btn:
            if not model_loaded:
                st.error("Model not loaded.")
            else:
                input_df = pd.DataFrame([{"age":age,"sex":sex,"chest pain type":chest_pain,"resting bp s":resting_bp,"cholesterol":cholesterol,"fasting blood sugar":fasting_bs,"resting ecg":resting_ecg,"max heart rate":max_hr,"exercise angina":exercise_angina,"oldpeak":oldpeak,"ST slope":st_slope}])
                input_df[["resting bp s","cholesterol","max heart rate","age"]] = std_scaler.transform(input_df[["resting bp s","cholesterol","max heart rate","age"]])
                input_df[["oldpeak"]] = mm_scaler.transform(input_df[["oldpeak"]])
                pred = model.predict(input_df)[0]
                prob = model.predict_proba(input_df)[0][1]
                risk = "High" if prob>0.7 else "Medium" if prob>0.4 else "Low"
                rcolor = {"High":"#E63946","Medium":"#D29922","Low":"#3FB950"}[risk]
                if pred==1:
                    st.markdown(f"<div class='result-positive'><div style='font-size:2.5rem'>⚠️</div><p class='result-title' style='color:#E63946'>Heart Disease<br>Detected</p><p style='opacity:0.7'>Confidence: {prob:.1%}</p><p style='color:{rcolor};font-weight:600'>{risk} Risk</p></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='result-negative'><div style='font-size:2.5rem'>✅</div><p class='result-title' style='color:#3FB950'>No Heart Disease<br>Detected</p><p style='opacity:0.7'>Confidence: {1-prob:.1%}</p><p style='color:{rcolor};font-weight:600'>{risk} Risk</p></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='border:1px dashed rgba(128,128,128,0.3);border-radius:10px;padding:3rem 1rem;text-align:center;opacity:0.6;'><div style='font-size:2rem;margin-bottom:1rem'>🫀</div><div style='font-size:0.85rem'>Fill in patient details<br>and click Analyze</div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE 3: DRIFT DETECTION
# ══════════════════════════════════════════════════════════════
elif page == "📊 Drift Detection":
    st.markdown("<div class='hero'><p class='hero-title'>Data <span>Drift</span> Monitoring</p><p class='hero-sub'>Detect when incoming patient data deviates from training distribution</p></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<p class='section-header'>Run Drift Detection</p>", unsafe_allow_html=True)
        st.markdown("<div style='border:1px solid rgba(128,128,128,0.2);border-radius:8px;padding:1.2rem;margin-bottom:1rem;font-size:0.85rem;line-height:1.7;background:rgba(128,128,128,0.03);'><b>How it works:</b><br>1. Compares reference vs current data<br>2. Evidently AI statistical tests per column<br>3. Flags drift if >20% columns show shift<br>4. Generates full visual HTML report</div>", unsafe_allow_html=True)
        if st.button("🔍 Run Drift Detection Now"):
            with st.spinner("Running Evidently drift analysis..."):
                try:
                    result = subprocess.run([sys.executable,"src/drift_detector.py"],capture_output=True,text=True,timeout=60)
                    output = result.stdout + result.stderr
                    st.markdown(f"<div class='log-box'>{output}</div>", unsafe_allow_html=True)
                    if "DRIFT DETECTED" in output:
                        st.error("⚠️ Drift Detected — Retraining Recommended")
                    else:
                        st.success("✅ No Drift — Model is Stable")
                except Exception as e:
                    st.error(f"Error: {e}")
    with col2:
        st.markdown("<p class='section-header'>Drift Report</p>", unsafe_allow_html=True)
        if os.path.exists("reports/drift_report.html"):
            with open("reports/drift_report.html","r") as f:
                st.components.v1.html(f.read(), height=500, scrolling=True)
        else:
            st.markdown("<div style='border:1px dashed rgba(128,128,128,0.3);border-radius:10px;padding:3rem 1rem;text-align:center;opacity:0.6;'><div style='font-size:2rem;margin-bottom:1rem'>📊</div><div style='font-size:0.85rem'>Run drift detection to<br>generate the report</div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE 4: RETRAIN PIPELINE
# ══════════════════════════════════════════════════════════════
elif page == "🔁 Retrain Pipeline":
    st.markdown("<div class='hero'><p class='hero-title'>Automated <span>Retraining</span> Pipeline</p><p class='hero-sub'>Trigger full ModelOps loop — drift check, retrain, evaluate, promote</p></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<p class='section-header'>Pipeline Steps</p>", unsafe_allow_html=True)
        for num,desc in [("01","Check data drift with Evidently AI"),("02","If drift > 20% → trigger retraining"),("03","Train new Random Forest model"),("04","Log run to MLflow experiment tracker"),("05","Compare accuracy against 85% threshold"),("06","Promote to Production if threshold met")]:
            st.markdown(f"<div class='pipeline-step'><span class='step-number'>{num}</span><span style='font-size:0.85rem'>{desc}</span></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Run Full Retraining Pipeline"):
            with st.spinner("Running automated retraining pipeline..."):
                try:
                    result = subprocess.run([sys.executable,"src/retrain_pipeline.py"],capture_output=True,text=True,timeout=120)
                    st.session_state["pipeline_output"] = result.stdout + result.stderr
                except Exception as e:
                    st.session_state["pipeline_output"] = f"Error: {e}"
    with col2:
        st.markdown("<p class='section-header'>Pipeline Output</p>", unsafe_allow_html=True)
        if "pipeline_output" in st.session_state:
            output = st.session_state["pipeline_output"]
            st.markdown(f"<div class='log-box'>{output}</div>", unsafe_allow_html=True)
            if "PIPELINE COMPLETE" in output:
                st.success("✅ Pipeline Completed Successfully")
            elif "Error" in output or "Traceback" in output:
                st.error("❌ Pipeline encountered an error")
        else:
            st.markdown("<div style='border:1px dashed rgba(128,128,128,0.3);border-radius:10px;padding:3rem 1rem;text-align:center;opacity:0.6;'><div style='font-size:2rem;margin-bottom:1rem'>🔁</div><div style='font-size:0.85rem'>Click the button to run<br>the full pipeline</div></div>", unsafe_allow_html=True)
        st.markdown("<br><div style='border:1px solid rgba(128,128,128,0.2);border-radius:8px;padding:1rem;background:rgba(128,128,128,0.03);'><p style='font-family:Space Mono,monospace;font-size:0.7rem;opacity:0.6;margin:0 0 0.5rem 0;'>AUTO-TRIGGER CONDITIONS</p><div style='font-size:0.82rem;line-height:1.8;'><div>📅 Every Monday at midnight (cron)</div><div>🔀 Every push to master branch</div><div>📊 When drift exceeds 20% threshold</div></div></div>", unsafe_allow_html=True)
