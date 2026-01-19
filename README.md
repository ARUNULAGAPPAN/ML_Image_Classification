# 🛡️ AURA: Neural Sentinel (v4.5)
### Advanced Real-Time Biometric Security & Liveness Detection System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" />
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg" />
  <img src="https://img.shields.io/badge/Engine-OpenCV--DNN-white.svg" />
  <img src="https://img.shields.io/badge/Security-Liveness--Verified-green.svg" />
</p>

> **AURA: Neural Sentinel** is a next-generation biometric access control system designed to defend against *presentation attacks* (spoofing) using **real-time liveness verification**.  
> Unlike traditional facial recognition systems that can be fooled by static images, AURA enforces a **physiological challenge-response mechanism** to guarantee human presence.

---

## 🚀 Key Features

### 🔐 Anti-Spoofing Protection
- Effectively blocks **print attacks**, **screen replay attacks**, and **photo-based impersonation**.

### 🧠 SFace Neural Recognition Engine
- Uses a **30MB ONNX-based SFace model**
- Produces **128-dimensional facial embeddings**
- Optimized for **low latency & high accuracy**

### 👄 Dynamic Liveness Challenge
- Requires the user to **open their mouth** in real time
- Detects internal mouth cavity using **intensity-based pixel analysis**

### 🎨 Ultra-Modern User Interface
- Built using **Streamlit** with injected **custom CSS**
- Features:
  - Deep violet gradient theme
  - Glassmorphism cards
  - Mobile-responsive layout

### 💫 Cyber-Scan Visual Feedback
- Animated **violet laser scan** during initialization
- Provides a futuristic, security-centric experience

---

## 🛠️ Tech Stack

| Category | Technology |
|-------|-----------|
| Language | Python |
| Frontend | Streamlit (Custom CSS) |
| Computer Vision | OpenCV (DNN Module) |
| Face Detection | YuNet |
| Face Recognition | SFace |
| Similarity Metric | Cosine Similarity |
| Liveness Logic | Binary Thresholding & Pixel Ratio Analysis |

---

## 📦 Installation & Setup

### 1️⃣ Clone the Repository

git clone https://github.com/yourusername/aura-neural-sentinel.git
cd aura-neural-sentinel





2️⃣ Install Dependencies
pip install streamlit opencv-python numpy pillow

3️⃣ Database Configuration

Place a clear, front-facing image of the authorized user in the root directory

Rename it to:

authorized_user.jpg

4️⃣ Initialize AI Models

Ensure the models/ directory contains:

models/
├── sface.onnx
└── face_detector.onnx

🖥️ Running the Application

Launch the system using:

streamlit run app.py

Runtime Flow:

Cyber-Scan animation initializes the system

Camera permission is requested

Identity verification is performed

Liveness challenge prompts the user to open their mouth

Upon success, secured data (e.g., Wi-Fi password) is revealed

🧠 Methodology
1️⃣ Facial Recognition Pipeline

Extracts 128-D facial embeddings using SFace

Compares live and stored vectors using Cosine Similarity

Access Threshold

Cosine Similarity > 0.40


(Configurable for sensitivity control)

2️⃣ Liveness Detection Algorithm

To confirm real human presence:

Detect face landmarks using YuNet

Define a Region of Interest (ROI) in the lower facial area

Apply Binary Thresholding to isolate the mouth cavity

Compute Dark Pixel Ratio

If ratio exceeds baseline by 15%, liveness is confirmed

✔️ This method prevents static image and replay-based spoofing

📂 Project Structure
├── models/
│   ├── sface.onnx            # Face Recognition Engine
│   └── face_detector.onnx    # Face Detection Engine
├── app.py                    # Main Application Logic
├── authorized_user.jpg       # Authorized User Database Image
└── README.md                 # Project Documentation

🏆 Presentation Demo Guide

When demonstrating to an audience or evaluator:

🔴 The Hack Attempt

Show a photo of yourself on a phone

System identifies the face but denies access

Status: Liveness Failed

🟢 The Real Access

Stand in front of the camera

Open your mouth

System instantly unlocks secured data

🧩 The Explanation

Prevents:

Print Attacks

Replay Attacks

Addresses the core vulnerability of traditional facial biometrics

🎓 Academic Context

Developed as part of the
AI / ML Image Classification Project – 2024

"Security is not a product, but a process."

👨‍💻 Author

S. Arun Ulagappan
Department of Computer Technology

⭐ If you find this project impactful, consider starring the repository.
🛡️ AURA stands for trust, verification, and intelligent defense.

