import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import pyttsx3
import threading
import time

# --- CONFIGURATION ---
# Ensure this matches the IP from your Arduino Serial Monitor
ESP32_URL = "http://192.168.4.1:81/stream" 
# ESP32_URL ="http://192.168.4.1:81/stream"

class SignLanguageDetector:
    def __init__(self, window):
        self.window = window
        self.window.title("ESP32-CAM Sign Language Detector")
        self.window.geometry("1000x800")
        self.window.configure(bg="#f0f0f0")

        # ------------------
        self.last_spoken_sign = None  # Prevents repeating the same word
        self.sign_counter = 0         # Counts frames to ensure sign is stable
        self.CONFIRM_THRESHOLD = 15   # Must see sign for 15 frames (~0.5s) to trigger
        # ---------------------------

        self.setup_styles()
        self.create_widgets()
        self.setup_variables()
        self.cap = None
        self.camera_thread = None

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", padding=10, font=("Arial", 12))
        style.configure("Header.TLabel", font=("Arial", 24, "bold"), foreground="#2c3e50", background="#f0f0f0")

    def create_widgets(self):
        header = ttk.Label(self.window, text="Sign Language Detector", style="Header.TLabel")
        header.pack(pady=20)

        self.video_frame = ttk.Frame(self.window, borderwidth=2, relief="groove")
        self.video_frame.pack(pady=10)

        self.video_label = ttk.Label(self.video_frame)
        self.video_label.pack()

        self.status_label = ttk.Label(self.window, text="Status: Waiting for Stream...", font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.detected_sign_label = ttk.Label(self.window, text="No sign detected", font=("Arial", 22, "bold"), foreground="#2980b9")
        self.detected_sign_label.pack(pady=10)

        self.start_button = ttk.Button(self.window, text="Start ESP32 Stream", command=self.toggle_detection)
        self.start_button.pack(pady=10)

    def setup_variables(self):
        self.is_detecting = False
        self.detected_sign = tk.StringVar(value="No sign detected")
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
        self.mpDraw = mp.solutions.drawing_utils
        self.finger_tips = [8, 12, 16, 20]

    def toggle_detection(self):
        if not self.is_detecting:
            self.start_detection()
        else:
            self.stop_detection()

    def start_detection(self):
        self.is_detecting = True
        self.start_button.config(text="Stop Stream")
        self.status_label.config(text=f"Status: Connecting to {ESP32_URL}")
        
        # Adding a timeout handling for VideoCapture
        self.cap = cv2.VideoCapture(ESP32_URL)
        
        if not self.camera_thread or not self.camera_thread.is_alive():
            self.camera_thread = threading.Thread(target=self.update_frame, daemon=True)
            self.camera_thread.start()

    def stop_detection(self):
        self.is_detecting = False
        self.start_button.config(text="Start ESP32 Stream")
        if self.cap:
            self.cap.release()

    def update_frame(self):
        while self.is_detecting:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    continue

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb_frame)

                current_frame_sign = "No sign detected"

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mpDraw.draw_landmarks(frame, hand_landmarks, self.mpHands.HAND_CONNECTIONS)
                        current_frame_sign = self.detect_sign(hand_landmarks)

                # --- ADVANCED LOGIC: Avoid Repetition & Handle Stability ---
                if current_frame_sign != "No sign detected":
                    # If we see the same sign as before, increase counter
                    if current_frame_sign == self.detected_sign.get():
                        self.sign_counter += 1
                    else:
                        # If a new sign is seen, reset counter to start verification
                        self.sign_counter = 0
                        self.detected_sign.set(current_frame_sign)

                    # Trigger Voice ONLY when sign is stable AND not just spoken
                    if self.sign_counter == self.CONFIRM_THRESHOLD:
                        if current_frame_sign != self.last_spoken_sign:
                            self.speak_text(current_frame_sign)
                            self.last_spoken_sign = current_frame_sign
                else:
                    # Reset if hand leaves the frame
                    self.sign_counter = 0
                    self.last_spoken_sign = None
                    self.detected_sign.set("No sign detected")

                # Update UI
                self.window.after(0, lambda: self.detected_sign_label.config(text=self.detected_sign.get()))
                
                # Convert for Tkinter
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                photo = ImageTk.PhotoImage(image=img)
                self.window.after(0, self.set_image, photo)

            except Exception as e:
                print(f"Error in stream: {e}")
                break

    def set_image(self, photo):
        self.video_label.config(image=photo)
        self.video_label.image = photo

    def detect_sign(self, hand_landmarks):
        lm = hand_landmarks.landmark
        # 1. HELP (All fingers up)
        if lm[8].y < lm[6].y and lm[12].y < lm[10].y and lm[16].y < lm[14].y and lm[20].y < lm[18].y and lm[4].y < lm[2].y:
            return 'HELP'
        # 2. Perfect (Thumb and Index up, others may vary)
        if lm[8].y > lm[6].y and lm[12].y < lm[10].y and lm[16].y < lm[14].y and lm[20].y < lm[18].y:
            return 'Perfect'
        # 3. Thank You (Palm toward face/camera logic)
        if lm[8].y < lm[6].y and lm[12].y < lm[10].y and lm[16].y > lm[14].y and lm[20].y > lm[18].y:
            return 'Thank You'
        # 4. Likes (Thumb Up)
        if lm[4].y < lm[3].y < lm[2].y and all(lm[tip].y > lm[tip-2].y for tip in [8,12,16,20]):
            return 'I Like it'
        
        return "No sign detected"

    def speak_text(self, text):
        def voice_worker():
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        threading.Thread(target=voice_worker, daemon=True).start()

    def close_app(self):
        self.is_detecting = False
        if self.cap: self.cap.release()
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SignLanguageDetector(root)
    root.mainloop()