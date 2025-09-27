#!/usr/bin/env python3
"""
Face Mask Detection with Camera
===============================
Real-time face mask detection using trained model
"""

import cv2
import numpy as np
import os
from pathlib import Path

def main():
    print("🎭 FACE MASK DETECTION - CAMERA TEST")
    print("=" * 40)
    
    # Look for the trained model
    model_paths = [
        "face_mask_detector_ready.h5",
        "../face_mask_detector_ready.h5", 
        "../../face_mask_detector_ready.h5"
    ]
    
    model = None
    model_path = None
    
    for path in model_paths:
        if Path(path).exists():
            model_path = path
            print(f"✅ Found model: {path}")
            break
    
    if model_path:
        try:
            import tensorflow as tf
            print("🔄 Loading model...")
            model = tf.keras.models.load_model(model_path)
            print("✅ Model loaded successfully!")
            print(f"📊 Model input shape: {model.input_shape}")
        except Exception as e:
            print(f"⚠️  Could not load model: {e}")
            model = None
    else:
        print("⚠️  No trained model found - using face detection only")
    
    # Initialize OpenCV
    print("\n📹 Setting up camera and face detection...")
    
    # Load face cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Cannot open camera")
        return
    
    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("✅ Camera ready!")
    print("\n🎮 CONTROLS:")
    print("   - Press 'q' to quit")
    print("   - Press 's' to save screenshot") 
    print("   - Press SPACE to toggle info display")
    
    show_info = True
    frame_count = 0
    
    print("\n🚀 Starting real-time detection...")
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
            
        frame_count += 1
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Process each detected face
        for (x, y, w, h) in faces:
            
            # Extract face region
            face_img = frame[y:y+h, x:x+w]
            
            label = "Face Detected"
            color = (255, 0, 0)  # Blue default
            confidence = 0.0
            
            # If model is loaded, make prediction
            if model is not None:
                try:
                    # Preprocess face for model
                    face_resized = cv2.resize(face_img, (224, 224))
                    face_array = np.expand_dims(face_resized, axis=0)
                    face_array = face_array / 255.0
                    
                    # Make prediction
                    prediction = model.predict(face_array, verbose=0)[0][0]
                    
                    # Interpret result (remember: mask=0, no_mask=1 from training)
                    if prediction < 0.5:  # Mask class
                        label = f"MASK"
                        color = (0, 255, 0)  # Green
                        confidence = 1 - prediction
                    else:  # No mask class
                        label = f"NO MASK"
                        color = (0, 0, 255)  # Red
                        confidence = prediction
                        
                    label += f" ({confidence:.2f})"
                    
                except Exception as e:
                    label = f"Error: {str(e)[:20]}..."
                    color = (0, 255, 255)  # Yellow
            
            # Draw modern bounding box with rounded corners effect
            thickness = 3
            # Main rectangle
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, thickness)
            
            # Corner accents for modern look
            corner_size = 15
            cv2.line(frame, (x, y), (x + corner_size, y), color, thickness + 2)
            cv2.line(frame, (x, y), (x, y + corner_size), color, thickness + 2)
            cv2.line(frame, (x + w, y), (x + w - corner_size, y), color, thickness + 2)
            cv2.line(frame, (x + w, y), (x + w, y + corner_size), color, thickness + 2)
            cv2.line(frame, (x, y + h), (x + corner_size, y + h), color, thickness + 2)
            cv2.line(frame, (x, y + h), (x, y + h - corner_size), color, thickness + 2)
            cv2.line(frame, (x + w, y + h), (x + w - corner_size, y + h), color, thickness + 2)
            cv2.line(frame, (x + w, y + h), (x + w, y + h - corner_size), color, thickness + 2)
            
            # Modern label background with transparency
            (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            label_y = y - 15
            if label_y < text_height + 10:
                label_y = y + h + text_height + 15
                
            # Semi-transparent background
            overlay = frame.copy()
            cv2.rectangle(overlay, (x, label_y - text_height - 8), (x + text_width + 16, label_y + 8), color, -1)
            cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
            
            # Clean label text
            cv2.putText(frame, label, (x + 8, label_y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Add clean info overlay
        if show_info:
            h, w = frame.shape[:2]
            
            # Semi-transparent background for info
            overlay = frame.copy()
            cv2.rectangle(overlay, (5, 5), (350, 90), (40, 40, 40), -1)
            cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
            
            # Modern info display
            info_y = 30
            cv2.putText(frame, f"AI Model: {'ACTIVE' if model else 'FACE ONLY'}", 
                       (15, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 255, 100) if model else (255, 255, 100), 2)
            
            cv2.putText(frame, f"Detections: {len(faces)} | Frame: {frame_count:,}", 
                       (15, info_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            # Clean controls at bottom
            cv2.rectangle(overlay, (w - 300, h - 35), (w - 5, h - 5), (40, 40, 40), -1)
            cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
            cv2.putText(frame, "Q:Quit  S:Save  SPACE:Toggle  ESC:Exit", 
                       (w - 295, h - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
        
        # Display frame
        cv2.imshow('Face Mask Detection - Clean Interface', frame)
        
        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:  # Q or ESC
            break
        elif key == ord('s'):
            filename = f"face_mask_detection_{frame_count:06d}.jpg"
            cv2.imwrite(filename, frame)
            print(f"📸 Screenshot saved: {filename}")
        elif key == ord(' '):  # Space bar
            show_info = not show_info
            print(f"ℹ️  Info display: {'ON' if show_info else 'OFF'}")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n📊 SESSION SUMMARY:")
    print(f"   - Total frames processed: {frame_count:,}")
    print(f"   - AI Model status: {'✅ Active' if model else '❌ Not loaded'}")
    if model:
        print(f"   - Model file: {model_path}")
    print("✅ Face mask detection session completed!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Detection stopped by user (Ctrl+C)")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()