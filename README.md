🛡️ AURA: Neural Sentinel (v4.5)
Advanced Real-Time Biometric Security & Liveness Detection
![alt text](https://img.shields.io/badge/Python-3.9+-blue.svg)

![alt text](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)

![alt text](https://img.shields.io/badge/Engine-OpenCV--DNN-white.svg)

![alt text](https://img.shields.io/badge/Security-Liveness--Verified-green.svg)
AURA: Neural Sentinel is a high-end biometric access control system designed to mitigate "Presentation Attacks" (spoofing). While standard facial recognition can be fooled by static photos, AURA utilizes Real-Time Liveness Detection, requiring the user to perform a specific physiological action—opening their mouth—to grant access.
🚀 Key Features
Anti-Spoofing Mechanism: Prevents unauthorized access via high-resolution photos or digital screens.
SFace Neural Engine: Utilizes an optimized 30MB ONNX-based Face Recognition model for high-speed, low-latency identification.
Dynamic Liveness Challenge: Implements a real-time "Open Mouth" classifier using Intensity Mapping.
Ultra-Modern UI: A custom-built, mobile-responsive dashboard featuring a deep-violet gradient theme and glassmorphism design.
Cyber-Scan Animation: Integrated visual feedback with a violet laser-scan effect during the initialization phase.
🛠️ Tech Stack
Language: Python
Frontend: Streamlit (Custom CSS-injected UI)
Computer Vision: OpenCV (DNN Module)
AI Models:
YuNet: For ultra-fast facial landmark detection.
SFace: For 128-dimensional facial feature extraction.
Math: Cosine Similarity & Binary Thresholding for liveness verification.
📦 Installation & Setup
Clone the repository:
code
Bash
git clone https://github.com/yourusername/aura-neural-sentinel.git
cd aura-neural-sentinel
Install dependencies:
code
Bash
pip install streamlit opencv-python numpy pillow
Database Configuration:
Place a clear, front-facing photo of the authorized user in the root directory.
Rename the photo to authorized_user.jpg.
Initialize Models:
Ensure the models/ folder contains sface.onnx and face_detector.onnx.
🖥️ Usage
Run the application using the following command:
code
Bash
streamlit run app.py
The system will display a Cyber-Scan animation.
Grant camera permissions.
The system will first verify your Identity.
Once identified, you must Open your mouth to satisfy the liveness challenge.
Upon success, the system reveals the encrypted data (e.g., Wifi Password).
🧠 Methodology
1. Facial Recognition
The system converts the input image into a 128-dimensional vector using the SFace model. It then calculates the Cosine Similarity between the live vector and the stored database vector.
Threshold: > 0.40 (Adjustable for sensitivity)
2. Liveness Detection
To detect an open mouth, the system:
Defines a Region of Interest (ROI) around the lower third of the detected face.
Applies Binary Thresholding to identify the dark void inside the mouth.
Calculates the Dark Pixel Ratio. If the ratio exceeds the baseline by 15%, liveness is confirmed.
📂 Project Structure
code
Text
├── models/
│   ├── sface.onnx            # AI Recognition Engine
│   └── face_detector.onnx    # AI Detection Engine
├── app.py                    # Main Application Code
├── authorized_user.jpg       # Database Photo (Authorized User)
└── README.md                 # Documentation
🏆 Presentation Demo Guide
When presenting to the class:
The Hack: Show a photo of yourself on your phone to the camera. The system will identify you but stay locked (Liveness Failed).
The Real Access: Step in front of the camera and open your mouth. The system will instantly reveal the password.
The Explanation: Explain that this prevents Replay Attacks and Print Attacks, which are the most common vulnerabilities in facial biometrics today.
Developed for AI/ML Image Classification Project 2024.
"Security is not a product, but a process."
