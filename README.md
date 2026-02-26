# **VaniSetu: The AI-Powered “Voice” Locket 🎙️🤟**

**VaniSetu** is an ultra-low-cost ($10) Edge-AI wearable designed to bridge the communication gap for **63 million hearing and speech-impaired individuals in India**.  

It converts **3D sign language gestures** into **real-time audible speech**, enabling independence and dignity — without bulky gloves or internet-dependent apps.

---

## 🛑 **The Problem**

### **Interpreter Scarcity**
- India has an estimated **1:28,000 ratio** of certified interpreters to deaf individuals.

### **Limitations of Existing Technology**
- **Smart Gloves**
  - Expensive (₹15k+)
  - Socially stigmatizing
  - Physically restrictive

- **Mobile Apps**
  - Require holding a phone (“third hand” problem)
  - Fail in offline or rural environments

---

## ✨ **The Solution — VaniSetu**

A lightweight, discreet **pendant (locket)** that digitizes the user’s signing space from a first-person perspective.

### **Key Features**
- ✅ 100% Offline (Access Point Mode — no internet required)
- ⚡ Ultra-Low Latency (<150 ms gesture-to-speech)
- 🎯 Dignified, fashion-forward wearable design

---

## 🛠️ **Technical Architecture**

### **1. Hardware Stack**
- **Controller:** ESP32-CAM (Wi-Fi + Bluetooth SoC)
- **Sensor:** OV2640 Wide-Angle Camera (120° FOV)
- **Power:** 3.7V Li-Po Battery + TP4056 USB-C Charging Module
- **Enclosure:** Custom lightweight 3D-printed chassis

### **2. Software & AI Pipeline**
- **Computer Vision:** MediaPipe Holistic (21-point hand landmark tracking)
- **Processing:** Edge-AI logic converts geometric coordinates into linguistic output
- **Communication:** Socket programming for fast data streaming
- **Speech Synthesis:** Python-based gTTS / pyttsx3 for instant audio output

---

## 🚀 **How It Works**

1. **Capture**  
   The locket camera faces the user’s hands and streams frames to a local processing unit (mobile/edge device).

2. **Analyze**  
   MediaPipe detects hand landmarks; Euclidean distances and angles are calculated to recognize signs.

3. **Speak**  
   Matched words or phrases are converted instantly into audio via Bluetooth earpiece or phone speaker.

---

## 📈 **Impact & Results**

- 💰 **97% cost reduction** compared to traditional assistive tech
- 🌐 Works in rural areas, hospitals, and low-connectivity environments
- 🔧 Modular system allows easy addition of Indian dialects (Hindi, Tamil, Marathi, etc.)

---

## 🛠️ **Installation & Setup**

```bash
# Clone repository
git clone https://github.com/BySimi/VaniSetu.git

# Install dependencies
pip install opencv-python mediapipe pyttsx3
