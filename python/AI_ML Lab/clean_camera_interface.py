#!/usr/bin/env python3
"""
Clean & Minimal Face Mask Detection Interface
============================================
Modern, minimal real-time face mask detection with clean UI
"""

import cv2
import numpy as np
import os
from pathlib import Path
import time

class CleanMaskDetector:
    def __init__(self):
        self.model = None
        self.face_cascade = None
        self.cap = None
        self.show_stats = False
        self.frame_count = 0
        self.fps = 0
        self.last_time = time.time()
        
        # UI Colors (BGR format)
        self.COLORS = {
            'mask': (20, 200, 20),      # Green
            'no_mask': (50, 50, 255),   # Red
            'face_only': (255, 165, 0), # Orange
            'text': (255, 255, 255),    # White
            'bg_dark': (0, 0, 0),       # Black
            'bg_semi': (40, 40, 40),    # Dark gray
            'accent': (100, 200, 255)   # Light blue
        }
        
    def load_model(self):
        """Load the trained face mask detection model"""
        model_paths = [
            "face_mask_detector_ready.h5",
            "Face_Mask_Detection_Complete_Project/face_mask_detector_ready.h5",
            "../face_mask_detector_ready.h5"
        ]
        
        for path in model_paths:
            if Path(path).exists():
                try:
                    import tensorflow as tf
                    tf.get_logger().setLevel('ERROR')  # Suppress TF logs
                    self.model = tf.keras.models.load_model(path, compile=False)
                    return True
                except Exception:
                    continue
        return False
    
    def setup_camera(self):
        """Initialize camera and face detection"""
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            return False
            
        # Set optimal resolution for performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        return True
    
    def predict_mask(self, face_img):
        """Predict mask/no-mask for a face region"""
        if self.model is None:
            return None, 0
            
        try:
            # Preprocess
            face_resized = cv2.resize(face_img, (224, 224))
            face_array = np.expand_dims(face_resized, axis=0) / 255.0
            
            # Predict
            prediction = self.model.predict(face_array, verbose=0)[0][0]
            
            if prediction < 0.5:
                return "MASK", 1 - prediction
            else:
                return "NO MASK", prediction
                
        except Exception:
            return None, 0
    
    def draw_detection_box(self, frame, x, y, w, h, label, confidence, color):
        """Draw clean detection box with label"""
        # Main bounding box
        thickness = 3
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, thickness)
        
        # Label background
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        font_thickness = 2
        
        if confidence > 0:
            text = f"{label} {confidence:.0%}"
        else:
            text = "FACE"
            
        (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)
        
        # Rounded background for label
        label_y = y - 15
        if label_y < text_h + 10:
            label_y = y + h + text_h + 15
            
        # Draw label background
        cv2.rectangle(frame, 
                     (x, label_y - text_h - 8), 
                     (x + text_w + 16, label_y + 8), 
                     color, -1)
        
        # Draw text
        cv2.putText(frame, text, (x + 8, label_y - 4), 
                   font, font_scale, self.COLORS['text'], font_thickness)
    
    def draw_clean_ui(self, frame):
        """Draw minimal UI overlay"""
        h, w = frame.shape[:2]
        
        if self.show_stats:
            # Semi-transparent background for stats
            overlay = frame.copy()
            cv2.rectangle(overlay, (10, 10), (300, 120), self.COLORS['bg_semi'], -1)
            cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
            
            # Status text
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, f"AI Model: {'ON' if self.model else 'OFF'}", 
                       (20, 35), font, 0.6, self.COLORS['accent'], 2)
            cv2.putText(frame, f"FPS: {self.fps:.1f}", 
                       (20, 60), font, 0.6, self.COLORS['text'], 2)
            cv2.putText(frame, f"Frame: {self.frame_count}", 
                       (20, 85), font, 0.6, self.COLORS['text'], 2)
        
        # Minimal controls at bottom
        controls = "Q:Quit  S:Save  SPACE:Stats  ESC:Exit"
        font = cv2.FONT_HERSHEY_SIMPLEX
        (text_w, text_h), _ = cv2.getTextSize(controls, font, 0.5, 1)
        
        # Background for controls
        cv2.rectangle(frame, 
                     (w - text_w - 20, h - text_h - 15), 
                     (w - 5, h - 5), 
                     self.COLORS['bg_semi'], -1)
        
        cv2.putText(frame, controls, 
                   (w - text_w - 15, h - 10), 
                   font, 0.5, self.COLORS['text'], 1)
    
    def update_fps(self):
        """Calculate and update FPS"""
        current_time = time.time()
        self.fps = 1.0 / (current_time - self.last_time)
        self.last_time = current_time
    
    def run(self):
        """Main detection loop"""
        print("🎭 Clean Face Mask Detection")
        print("=" * 30)
        
        # Initialize components
        model_loaded = self.load_model()
        if not self.setup_camera():
            print("❌ Cannot access camera")
            return
            
        print(f"✅ Model: {'Loaded' if model_loaded else 'Face detection only'}")
        print("✅ Camera ready")
        print("\n🚀 Starting detection... (Press Q to quit)")
        
        # Create window
        cv2.namedWindow('Face Mask Detection - Clean UI', cv2.WINDOW_AUTOSIZE)
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                self.frame_count += 1
                self.update_fps()
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Convert to grayscale for face detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detect faces
                faces = self.face_cascade.detectMultiScale(
                    gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60)
                )
                
                # Process each face
                for (x, y, w, h) in faces:
                    face_img = frame[y:y+h, x:x+w]
                    
                    if self.model:
                        label, confidence = self.predict_mask(face_img)
                        if label == "MASK":
                            color = self.COLORS['mask']
                        elif label == "NO MASK":
                            color = self.COLORS['no_mask']
                        else:
                            color = self.COLORS['face_only']
                            label = "FACE"
                            confidence = 0
                    else:
                        label = "FACE"
                        confidence = 0
                        color = self.COLORS['face_only']
                    
                    # Draw detection
                    self.draw_detection_box(frame, x, y, w, h, label, confidence, color)
                
                # Draw UI
                self.draw_clean_ui(frame)
                
                # Display frame
                cv2.imshow('Face Mask Detection - Clean UI', frame)
                
                # Handle input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:  # Q or ESC
                    break
                elif key == ord('s'):
                    filename = f"mask_detection_{int(time.time())}.jpg"
                    cv2.imwrite(filename, frame)
                    print(f"📸 Saved: {filename}")
                elif key == ord(' '):  # Space
                    self.show_stats = not self.show_stats
                    
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print(f"\n📊 Session: {self.frame_count:,} frames processed")
        print("✅ Clean exit")

def main():
    detector = CleanMaskDetector()
    detector.run()

if __name__ == "__main__":
    main()