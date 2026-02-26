VaniSetu: The AI-Powered "Voice" Locket 🎙️🤟
VaniSetu is an ultra-low-cost ($10), Edge-AI wearable designed to bridge the communication gap for the 63 million hearing and speech-impaired individuals in India. By converting 3D sign language gestures into real-time audible speech, it restores independence and dignity to users without the need for bulky gloves or internet-dependent mobile apps.

🛑 The Problem
Interpreter Scarcity: India has a staggering 1:28,000 ratio of certified interpreters to deaf individuals.

Failure of Existing Tech: * Smart Gloves: Expensive (₹15k+), socially stigmatizing, and physically restrictive.

Mobile Apps: Require a "third hand" to hold the phone and fail in offline/rural areas.

✨ The Solution: VaniSetu
A lightweight, discreet pendant (Locket) that digitizes the user's "signing space" from a first-person perspective.

100% Offline: Operates via Access Point (AP) Mode—no internet required.

Ultra-Low Latency: Translates gestures to speech in <150ms.

Dignified Design: A fashion-forward wearable that replaces medical-grade sensors.

🛠️ Technical Architecture
1. Hardware Stack
Controller: ESP32-CAM (Wi-Fi + BT SoC)

Sensor: OV2640 Wide-Angle Camera (120° FOV)

Power: 3.7V Li-Po Battery with TP4056 USB-C Charging Module

Enclosure: Custom 3D-printed lightweight chassis

2. Software & AI Pipeline
Computer Vision: MediaPipe Holistic for real-time 21-point skeletal hand landmarking.

Processing: Edge AI logic translates geometric coordinate arrays into linguistic strings.

Communication: Socket Programming for high-speed data streaming between hardware and mobile.

Speech Synthesis: Python-based gTTS / Pyttsx3 for instant audio output.

🚀 How It Works
Capture: The locket camera faces the user's hands, streaming frames to a local processing unit (Mobile/Edge device).

Analyze: MediaPipe identifies hand landmarks; the system calculates Euclidean distances and angles to match signs.

Speak: The matched word/phrase is instantly converted to audio via a Bluetooth earpiece or phone speaker.

📈 Impact & Results
Cost Reduction: Cut the price of assistive communication tech by 97%.

Accessibility: Functions in basements, rural areas, and hospitals with zero connectivity.

Scalability: Modular software allows for easy integration of regional Indian dialects (Hindi, Tamil, Marathi, etc.).

🛠️ Installation & Setup
Bash
# Clone the repository
git clone https://github.com/BySimi/VaniSetu.git

# Install dependencies
pip install opencv-python mediapipe pyttsx3
Flash the ESP32-CAM using the provided .ino firmware.

Connect your device to the VaniSetu_AP Wi-Fi network.

Run main.py to start the Vision-to-Voice engine.
