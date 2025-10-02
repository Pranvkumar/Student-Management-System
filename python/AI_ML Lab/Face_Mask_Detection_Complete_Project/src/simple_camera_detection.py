#!/usr/bin/env python3
"""
Simple Real-Time Face Mask Detection
====================================
Direct camera connection with mask detection
"""

import cv2
import numpy as np
import os
from pathlib import Path

def simple_face_mask_detection():
    """Simple real-time face mask detection"""
    
    print("🎭 SIMPLE REAL-TIME FACE MASK DETECTION")
    print("=" * 42)
    
    # Check if trained model exists
    model_paths = [
        "../../face_mask_detector_ready.h5",
        "../../../face_mask_detector_ready.h5",
        "face_mask_detector_ready.h5",
        "face_mask_detector_trained.h5"
    ]
    
    model_path = None
    for path in model_paths:
        if Path(path).exists():
            model_path = path
            break
    
    model_available = model_path is not None
    
    if model_available:
        print(f"✅ Found trained model: {model_path}")
        try:
            import tensorflow as tf
            model = tf.keras.models.load_model(model_path)
            print("✅ Model loaded successfully!")
            model_loaded = True
        except Exception as e:
            print(f"⚠️  Could not load model: {e}")
            print("🔧 Will use face detection only")
            model_loaded = False
            model = None
    else:
        print("⚠️  No trained model found")
        print("🔧 Will use face detection only")
        model_loaded = False
        model = None
    
    # Initialize face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    if face_cascade.empty():
        print("❌ Could not load face detection")
        return
    
    print("✅ Face detection ready")
    
    # Initialize camera
    print("\n📹 Initializing camera...")
    cap = cv2.VideoCapture(0)  # Use camera 0
    
    if not cap.isOpened():
        print("❌ Could not open camera")
        print("💡 Try camera indices 1, 2, etc.")
        return
    
    print("✅ Camera opened successfully!")
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("\n🚀 Starting real-time detection...")
    print("🎮 Controls:")
    print("   - Press 'q' to quit")
    print("   - Press 's' to save screenshot")
    
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("❌ Could not read frame")
            break
        
        frame_count += 1
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Process each face
        for (x, y, w, h) in faces:
            # Extract face region
            face_img = frame[y:y+h, x:x+w]
            
            if model_loaded and model is not None:
                try:
                    # Preprocess face for model
                    face_resized = cv2.resize(face_img, (224, 224))
                    face_array = np.expand_dims(face_resized, axis=0)
                    face_array = face_array / 255.0
                    
                    # Make prediction
                    prediction = model.predict(face_array, verbose=0)[0][0]
                    
                    # Determine result
                    if prediction > 0.5:
                        label = f"Mask ({prediction:.2f})"
                        color = (0, 255, 0)  # Green
                    else:
                        label = f"No Mask ({1-prediction:.2f})"
                        color = (0, 0, 255)  # Red
                        
                except Exception as e:
                    label = "Face Detected"
                    color = (255, 0, 0)  # Blue
            else:
                label = "Face Detected"
                color = (255, 0, 0)  # Blue
            
            # Draw rectangle and label
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            # Add background for text
            (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(frame, (x, y-text_height-10), (x+text_width, y), color, -1)
            
            # Add text
            cv2.putText(frame, label, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Add info overlay
        status = "AI Model Active" if model_loaded else "Face Detection Only"
        cv2.putText(frame, f"Status: {status}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        cv2.putText(frame, f"Faces: {len(faces)} | Frame: {frame_count}", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Display frame
        cv2.imshow('Face Mask Detection - Real Time', frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            screenshot_name = f"face_mask_detection_{frame_count:04d}.jpg"
            cv2.imwrite(screenshot_name, frame)
            print(f"📸 Screenshot saved: {screenshot_name}")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n📊 Session Summary:")
    print(f"   - Frames processed: {frame_count}")
    print(f"   - AI Model: {'✅ Active' if model_loaded else '❌ Not available'}")
    print("✅ Detection session completed!")

if __name__ == "__main__":
    try:
        simple_face_mask_detection()
    except KeyboardInterrupt:
        print("\n👋 Detection stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Check camera connection and model files")