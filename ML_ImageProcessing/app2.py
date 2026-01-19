import streamlit as st
import cv2
import numpy as np
import os
from PIL import Image
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="AURA SENTINEL", layout="wide", initial_sidebar_state="collapsed")

# --- ADVANCED CSS (Mobile Optimized + Animations) ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Deep Obsidian & Violet Theme */
    .stApp {
        background: radial-gradient(circle at center, #12002b 0%, #050505 100%);
        color: #e0e0e0;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* Professional Title */
    .main-title {
        background: linear-gradient(to bottom, #a855f7, #4c1d95);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3rem;
        font-weight: 900;
        margin-bottom: 0px;
        letter-spacing: -1px;
    }
    
    .sub-title {
        text-align: center;
        color: #8A2BE2;
        font-size: 10px;
        letter-spacing: 4px;
        margin-bottom: 30px;
        opacity: 0.8;
    }

    /* Animation: Violet Scanning Pulse */
    @keyframes scan {
        0% { top: 0%; opacity: 0; }
        50% { opacity: 1; }
        100% { top: 100%; opacity: 0; }
    }

    .scanner-overlay {
        position: relative;
        width: 100%;
        height: 300px;
        border: 1px solid #4c1d95;
        border-radius: 15px;
        overflow: hidden;
        background: rgba(138, 43, 226, 0.05);
        margin-bottom: 20px;
    }

    .scan-line {
        position: absolute;
        width: 100%;
        height: 4px;
        background: #a855f7;
        box-shadow: 0 0 15px #a855f7;
        animation: scan 2s linear infinite;
    }

    .loading-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: #a855f7;
        font-weight: bold;
        letter-spacing: 2px;
        font-size: 12px;
    }

    /* Mobile Responsive Status Cards */
    .status-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
        margin-top: 15px;
    }

    .status-card {
        background: rgba(20, 0, 40, 0.8);
        border: 1px solid #4c1d95;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        flex: 1;
        min-width: 140px;
    }

    /* Access Banner (No Glow) */
    .access-granted {
        background: #4c1d95;
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        margin-top: 20px;
        border: 1px solid #a855f7;
    }

    .wifi-reveal {
        background: rgba(34, 197, 94, 0.1);
        border: 1px dashed #22c55e;
        color: #22c55e;
        padding: 15px;
        margin-top: 10px;
        border-radius: 10px;
        text-align: center;
        font-family: monospace;
        font-size: 18px;
    }

    /* Mobile Adjustments */
    @media (max-width: 640px) {
        .main-title { font-size: 2.2rem; }
        .status-card { min-width: 100%; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- MODELS (CORE DNN) ---
MODELS_DIR = "models"
SFACE_PATH = os.path.join(MODELS_DIR, "sface.onnx")
YUNET_PATH = os.path.join(MODELS_DIR, "face_detector.onnx")

@st.cache_resource
def load_nets():
    if not os.path.exists(SFACE_PATH) or not os.path.exists(YUNET_PATH):
        return None, None
    return cv2.dnn.readNet(YUNET_PATH), cv2.dnn.readNet(SFACE_PATH)

detector_net, recognizer_net = load_nets()

# --- AI LOGIC ---
def get_ai_features(img):
    if detector_net is None: return None, None
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces) > 0:
        x, y, w_f, h_f = faces[0]
        face_img = img[y:y+h_f, x:x+w_f]
        face_img = cv2.resize(face_img, (112, 112))
        rec_blob = cv2.dnn.blobFromImage(face_img, 1.0, (112, 112), (0, 0, 0), False, False)
        recognizer_net.setInput(rec_blob)
        return recognizer_net.forward().flatten(), (x, y, w_f, h_f)
    return None, None

# --- DATABASE ---
AUTH_IMG_PATH = "authorized_user.jpg"
if not os.path.exists(AUTH_IMG_PATH):
    st.error("MISSING DATABASE IMAGE")
    st.stop()

auth_bgr = cv2.imread(AUTH_IMG_PATH)
AUTH_FEATURES, _ = get_ai_features(auth_bgr)

# --- UI START ---
st.markdown("<h1 class='main-title'>AURA</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>NEURAL SENTINEL BIOMETRICS</p>", unsafe_allow_html=True)

col_l, col_mid, col_r = st.columns([1, 4, 1])

with col_mid:
    img_file = st.camera_input("")
    if img_file:
        img = Image.open(img_file)
        frame_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        curr_features, face_box = get_ai_features(frame_bgr)
        id_ok = False
        live_ok = False
        if curr_features is not None:
            sim = np.dot(AUTH_FEATURES, curr_features) / (np.linalg.norm(AUTH_FEATURES) * np.linalg.norm(curr_features))
            st.markdown("<div class='status-container'>", unsafe_allow_html=True)
            # Identity Check
            if sim > 0.4:
                id_ok = True
                st.markdown("<div class='status-card'><small>IDENTITY</small><br><b style='color:#22c55e;'>CONFIRMED</b></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='status-card'><small>IDENTITY</small><br><b style='color:#ef4444;'>UNKNOWN</b></div>", unsafe_allow_html=True)
            # Liveness Check
            if id_ok:
                x, y, w, h = face_box
                mouth_roi = frame_bgr[y + int(h*0.7):y + h, x + int(w*0.25):x + int(w*0.75)]
                gray_mouth = cv2.cvtColor(mouth_roi, cv2.COLOR_BGR2GRAY)
                _, thr = cv2.threshold(gray_mouth, 50, 255, cv2.THRESH_BINARY_INV)
                ratio = cv2.countNonZero(thr) / (mouth_roi.shape[0] * mouth_roi.shape[1])
                if ratio > 0.15:
                    live_ok = True
                    st.markdown("<div class='status-card'><small>LIVENESS</small><br><b style='color:#22c55e;'>SUCCESS</b></div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='status-card'><small>LIVENESS</small><br><b style='color:#f59e0b;'>OPEN MOUTH</b></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            # Final Success
            if id_ok and live_ok:
                st.markdown("<div class='access-granted'>ACCESS GRANTED</div>", unsafe_allow_html=True)
                st.markdown("<div class='wifi-reveal'>📶 Wifi password is <b>12345678</b></div>", unsafe_allow_html=True)
                st.balloons()
        else:
            st.markdown("<div class='status-card' style='width:100%'>FACE NOT DETECTED IN OPTIC SENSOR</div>", unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; color:#4c1d95; font-size:10px;'>AURA v4.5 SECURE ACCESS POINT</p>", unsafe_allow_html=True)