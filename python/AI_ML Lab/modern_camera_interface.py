#!/usr/bin/env python3
"""
Ultra-Clean Face Mask Detection Interface
========================================
Modern, minimal interface with sleek design and smooth animations
"""

import cv2
import numpy as np
import os
from pathlib import Path
import time
import math

class ModernMaskDetector:
    def __init__(self):
        self.model = None
        self.face_cascade = None
        self.cap = None
        
        # UI State
        self.show_overlay = True
        self.frame_count = 0
        self.fps = 0
        self.last_time = time.time()
        self.detection_count = {'mask': 0, 'no_mask': 0, 'face': 0}
        
        # Animation variables
        self.pulse_phase = 0
        self.fade_alpha = 0.8
        
        # Modern color palette (BGR)
        self.THEME = {
            'mask_safe': (85, 255, 85),      # Bright green
            'mask_danger': (50, 50, 255),    # Bright red  
            'face_neutral': (255, 200, 100), # Light blue
            'text_primary': (255, 255, 255), # White
            'text_secondary': (200, 200, 200), # Light gray
            'background': (25, 25, 25),      # Dark background
            'accent': (255, 150, 50),        # Orange accent
            'success': (100, 255, 100),      # Success green
            'warning': (100, 200, 255)       # Warning yellow
        }
        
    def load_model(self):
        """Load AI model with error handling"""
        model_candidates = [
            "face_mask_detector_ready.h5",
            "Face_Mask_Detection_Complete_Project/face_mask_detector_ready.h5",
            "../face_mask_detector_ready.h5",
            "Face_Mask_Detection_Complete_Project/models/face_mask_detector_ready.h5"
        ]
        
        for path in model_candidates:
            if Path(path).exists():
                try:
                    import tensorflow as tf
                    # Suppress TensorFlow warnings
                    tf.get_logger().setLevel('ERROR')
                    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
                    
                    self.model = tf.keras.models.load_model(path, compile=False)
                    return path
                except Exception as e:
                    continue
        return None
    
    def setup_camera(self):
        """Initialize camera with optimal settings"""
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            return False
            
        # Optimize camera settings
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        return True
    
    def predict_mask_status(self, face_region):
        """AI prediction with confidence scoring"""
        if self.model is None:
            return "DETECTING", 0.0, "face"
            
        try:
            # Preprocess face
            processed_face = cv2.resize(face_region, (224, 224))
            face_array = np.expand_dims(processed_face, axis=0) / 255.0
            
            # Get prediction
            prediction = self.model.predict(face_array, verbose=0)[0][0]
            
            if prediction < 0.5:  # Mask detected
                confidence = (1 - prediction) * 100
                return "MASK DETECTED", confidence, "mask"
            else:  # No mask
                confidence = prediction * 100
                return "NO MASK", confidence, "no_mask"
                
        except Exception:
            return "AI ERROR", 0.0, "face"
    
    def draw_modern_detection_box(self, frame, x, y, w, h, status, confidence, detection_type):
        """Draw sleek, modern detection box"""
        
        # Choose colors based on detection
        if detection_type == "mask":
            primary_color = self.THEME['mask_safe']
            bg_color = (*self.THEME['mask_safe'], 40)
        elif detection_type == "no_mask":
            primary_color = self.THEME['mask_danger']
            bg_color = (*self.THEME['mask_danger'], 40)
        else:
            primary_color = self.THEME['face_neutral']
            bg_color = (*self.THEME['face_neutral'], 40)
        
        # Add pulsing effect for high confidence detections
        if confidence > 80:
            pulse = int(20 * math.sin(self.pulse_phase))
            primary_color = tuple(min(255, c + pulse) for c in primary_color)
        
        # Modern rounded corners effect (simulate with multiple rectangles)
        thickness = 3
        corner_size = 20
        
        # Main bounding box with rounded corners simulation
        # Top line
        cv2.line(frame, (x + corner_size, y), (x + w - corner_size, y), primary_color, thickness)
        # Bottom line  
        cv2.line(frame, (x + corner_size, y + h), (x + w - corner_size, y + h), primary_color, thickness)
        # Left line
        cv2.line(frame, (x, y + corner_size), (x, y + h - corner_size), primary_color, thickness)
        # Right line
        cv2.line(frame, (x + w, y + corner_size), (x + w, y + h - corner_size), primary_color, thickness)
        
        # Corner curves (simple diagonal lines for rounded effect)
        cv2.line(frame, (x, y + corner_size), (x + corner_size, y), primary_color, thickness)
        cv2.line(frame, (x + w - corner_size, y), (x + w, y + corner_size), primary_color, thickness)
        cv2.line(frame, (x, y + h - corner_size), (x + corner_size, y + h), primary_color, thickness)
        cv2.line(frame, (x + w - corner_size, y + h), (x + w, y + h - corner_size), primary_color, thickness)
        
        # Status label with modern styling
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        font_thickness = 2
        
        if confidence > 0:
            label_text = f"{status}"
            confidence_text = f"{confidence:.0f}%"
        else:
            label_text = status
            confidence_text = ""
        
        # Calculate text dimensions
        (label_w, label_h), _ = cv2.getTextSize(label_text, font, font_scale, font_thickness)
        (conf_w, conf_h), _ = cv2.getTextSize(confidence_text, font, font_scale - 0.2, font_thickness - 1)
        
        # Position label above box
        label_y = y - 15
        if label_y < label_h + 20:
            label_y = y + h + label_h + 20
            
        # Modern label background with transparency effect
        overlay = frame.copy()
        label_bg_width = max(label_w, conf_w) + 20
        cv2.rectangle(overlay, 
                     (x, label_y - label_h - 15), 
                     (x + label_bg_width, label_y + 10), 
                     primary_color, -1)
        cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
        
        # Draw text
        cv2.putText(frame, label_text, (x + 10, label_y - 8), 
                   font, font_scale, self.THEME['text_primary'], font_thickness)
        
        if confidence_text:
            cv2.putText(frame, confidence_text, (x + 10, label_y + 5), 
                       font, font_scale - 0.2, self.THEME['text_secondary'], font_thickness - 1)
    
    def draw_sleek_overlay(self, frame):
        """Draw modern, minimal overlay interface"""
        h, w = frame.shape[:2]
        
        if not self.show_overlay:
            return
        
        # Top status bar
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, 80), self.THEME['background'], -1)
        cv2.addWeighted(overlay, self.fade_alpha, frame, 1 - self.fade_alpha, 0, frame)
        
        # App title
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, "FACE MASK AI", (20, 30), 
                   font, 0.8, self.THEME['accent'], 2)
        
        # AI Status indicator
        ai_status = "AI ACTIVE" if self.model else "FACE ONLY"
        ai_color = self.THEME['success'] if self.model else self.THEME['warning']
        cv2.putText(frame, ai_status, (20, 55), 
                   font, 0.5, ai_color, 2)
        
        # Performance metrics (top right)
        fps_text = f"FPS: {self.fps:.1f}"
        cv2.putText(frame, fps_text, (w - 150, 30), 
                   font, 0.6, self.THEME['text_primary'], 2)
        
        frame_text = f"Frame: {self.frame_count:,}"
        cv2.putText(frame, frame_text, (w - 150, 55), 
                   font, 0.5, self.THEME['text_secondary'], 2)
        
        # Detection statistics (bottom left)
        stats_y = h - 100
        total_detections = sum(self.detection_count.values())
        
        if total_detections > 0:
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, stats_y), (300, h), self.THEME['background'], -1)
            cv2.addWeighted(overlay, self.fade_alpha, frame, 1 - self.fade_alpha, 0, frame)
            
            cv2.putText(frame, "SESSION STATS", (20, stats_y + 25), 
                       font, 0.5, self.THEME['accent'], 2)
            
            mask_pct = (self.detection_count['mask'] / total_detections) * 100 if total_detections > 0 else 0
            cv2.putText(frame, f"Mask: {self.detection_count['mask']} ({mask_pct:.1f}%)", 
                       (20, stats_y + 50), font, 0.45, self.THEME['mask_safe'], 2)
            
            no_mask_pct = (self.detection_count['no_mask'] / total_detections) * 100 if total_detections > 0 else 0
            cv2.putText(frame, f"No Mask: {self.detection_count['no_mask']} ({no_mask_pct:.1f}%)", 
                       (20, stats_y + 70), font, 0.45, self.THEME['mask_danger'], 2)
        
        # Modern control hints (bottom right)
        controls = ["Q: Quit", "S: Save", "H: Toggle UI", "ESC: Exit"]
        control_x = w - 180
        
        for i, control in enumerate(controls):
            cv2.putText(frame, control, (control_x, h - 80 + (i * 18)), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.THEME['text_secondary'], 1)
    
    def update_metrics(self):
        """Update FPS and animation variables"""
        current_time = time.time()
        self.fps = 1.0 / (current_time - self.last_time) if self.last_time else 0
        self.last_time = current_time
        self.pulse_phase += 0.2
    
    def run_detection(self):
        """Main detection loop with modern UI"""
        print("🚀 Modern Face Mask Detection Interface")
        print("=" * 45)
        
        # Initialize systems
        model_path = self.load_model()
        camera_ready = self.setup_camera()
        
        if not camera_ready:
            print("❌ Camera initialization failed")
            return
            
        print(f"✅ AI Model: {'Loaded' if model_path else 'Face detection only'}")
        if model_path:
            print(f"   📄 Model: {os.path.basename(model_path)}")
        print("✅ Camera: Ready")
        print("\n🎮 Controls: Q=Quit, S=Save, H=Toggle UI, ESC=Exit")
        print("🔄 Starting detection...\n")
        
        # Create modern window
        window_name = "Face Mask AI - Modern Interface"
        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                self.frame_count += 1
                self.update_metrics()
                
                # Mirror effect for natural interaction
                frame = cv2.flip(frame, 1)
                
                # Face detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(
                    gray, 
                    scaleFactor=1.1, 
                    minNeighbors=6, 
                    minSize=(80, 80),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )
                
                # Process detected faces
                for (x, y, w, h) in faces:
                    face_region = frame[y:y+h, x:x+w]
                    status, confidence, detection_type = self.predict_mask_status(face_region)
                    
                    # Update statistics
                    if detection_type in self.detection_count:
                        self.detection_count[detection_type] += 1
                    
                    # Draw modern detection box
                    self.draw_modern_detection_box(frame, x, y, w, h, status, confidence, detection_type)
                
                # Draw sleek interface
                self.draw_sleek_overlay(frame)
                
                # Display frame
                cv2.imshow(window_name, frame)
                
                # Handle user input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:  # Q or ESC
                    break
                elif key == ord('s'):  # Save screenshot
                    timestamp = int(time.time())
                    filename = f"mask_detection_modern_{timestamp}.jpg"
                    cv2.imwrite(filename, frame)
                    print(f"📸 Screenshot saved: {filename}")
                elif key == ord('h'):  # Toggle UI
                    self.show_overlay = not self.show_overlay
                    print(f"🎨 UI Overlay: {'ON' if self.show_overlay else 'OFF'}")
                    
        except KeyboardInterrupt:
            print("\n⏹️  Detection stopped by user")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean shutdown"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        
        # Final statistics
        print(f"\n📊 FINAL STATISTICS:")
        print(f"   🎞️  Total frames: {self.frame_count:,}")
        print(f"   ⚡ Average FPS: {self.fps:.1f}")
        print(f"   ✅ Mask detections: {self.detection_count['mask']:,}")
        print(f"   ❌ No-mask detections: {self.detection_count['no_mask']:,}")
        print(f"   👤 Face-only detections: {self.detection_count['face']:,}")
        print("✨ Modern Face Mask Detection completed!")

def main():
    detector = ModernMaskDetector()
    detector.run_detection()

if __name__ == "__main__":
    main()