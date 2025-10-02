#!/usr/bin/env python3
"""
Real-Time Face Mask Detection with Camera
========================================
Connect camera to face mask detection model for live testing
"""

import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import os
from pathlib import Path

class RealTimeFaceMaskDetector:
    def __init__(self, model_path=None):
        """Initialize the real-time face mask detector"""
        
        print("🎭 INITIALIZING REAL-TIME FACE MASK DETECTOR")
        print("=" * 48)
        
        # Initialize face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Load or create mask detection model
        self.mask_model = self.load_or_create_model(model_path)
        
        # Detection parameters
        self.confidence_threshold = 0.5
        
        print("✅ Real-time detector initialized!")
    
    def load_or_create_model(self, model_path):
        """Load existing model or create a simple one for demonstration"""
        
        if model_path and Path(model_path).exists():
            print(f"📁 Loading model from: {model_path}")
            try:
                model = load_model(model_path)
                print("✅ Model loaded successfully!")
                return model
            except Exception as e:
                print(f"❌ Error loading model: {e}")
        
        print("🤖 Creating demonstration model...")
        return self.create_demo_model()
    
    def create_demo_model(self):
        """Create a simple demonstration model"""
        
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
        from tensorflow.keras.applications import MobileNetV2
        from tensorflow.keras.layers import GlobalAveragePooling2D
        
        print("🏗️  Building MobileNetV2-based model...")
        
        # Create base model
        base_model = MobileNetV2(
            weights='imagenet',
            include_top=False,
            input_shape=(224, 224, 3)
        )
        
        # Freeze base model
        base_model.trainable = False
        
        # Add custom layers
        model = Sequential([
            base_model,
            GlobalAveragePooling2D(),
            Dense(128, activation='relu'),
            Dropout(0.5),
            Dense(1, activation='sigmoid')  # Binary classification
        ])
        
        # Compile model
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        print("✅ Demo model created (untrained - for structure testing)")
        print("⚠️  Note: This model is untrained. For real detection, train with your dataset!")
        
        return model
    
    def preprocess_face(self, face_img):
        """Preprocess face image for model prediction"""
        
        # Resize to model input size
        face_resized = cv2.resize(face_img, (224, 224))
        
        # Convert to array and normalize
        face_array = img_to_array(face_resized)
        face_array = np.expand_dims(face_array, axis=0)
        face_array = face_array / 255.0  # Normalize to [0,1]
        
        return face_array
    
    def predict_mask(self, face_img):
        """Predict if face has mask or not"""
        
        try:
            # Preprocess face
            processed_face = self.preprocess_face(face_img)
            
            # Make prediction
            prediction = self.mask_model.predict(processed_face, verbose=0)
            confidence = float(prediction[0][0])
            
            # Determine label (assuming 0=no_mask, 1=with_mask)
            if confidence > self.confidence_threshold:
                label = "Mask"
                color = (0, 255, 0)  # Green
            else:
                label = "No Mask"
                color = (0, 0, 255)  # Red
                confidence = 1 - confidence  # Flip confidence for no mask
            
            return label, confidence, color
            
        except Exception as e:
            print(f"⚠️  Prediction error: {e}")
            return "Unknown", 0.0, (128, 128, 128)
    
    def detect_faces_and_masks(self, frame):
        """Detect faces and predict mask status"""
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(30, 30)
        )
        
        results = []
        
        for (x, y, w, h) in faces:
            # Extract face region
            face_img = frame[y:y+h, x:x+w]
            
            # Predict mask status
            label, confidence, color = self.predict_mask(face_img)
            
            results.append({
                'bbox': (x, y, w, h),
                'label': label,
                'confidence': confidence,
                'color': color
            })
        
        return results
    
    def draw_predictions(self, frame, results):
        """Draw bounding boxes and predictions on frame"""
        
        for result in results:
            x, y, w, h = result['bbox']
            label = result['label']
            confidence = result['confidence']
            color = result['color']
            
            # Draw bounding box
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            # Create label text
            text = f"{label}: {confidence:.2f}"
            
            # Get text size for background
            (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            
            # Draw background rectangle for text
            cv2.rectangle(frame, (x, y-text_height-10), (x+text_width, y), color, -1)
            
            # Draw text
            cv2.putText(frame, text, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return frame
    
    def start_camera_detection(self, camera_index=0):
        """Start real-time camera detection"""
        
        print(f"\n📹 STARTING REAL-TIME CAMERA DETECTION")
        print("=" * 40)
        print("🎮 Controls:")
        print("   - Press 'q' to quit")
        print("   - Press 's' to save screenshot")
        print("   - Press 'SPACE' to pause/unpause")
        print("   - Press 'r' to reset/restart")
        
        # Initialize camera
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print(f"❌ Error: Could not open camera {camera_index}")
            print("💡 Try different camera indices (0, 1, 2...)")
            return
        
        print(f"✅ Camera {camera_index} opened successfully!")
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        paused = False
        frame_count = 0
        screenshot_count = 0
        
        print("\n🚀 Starting detection loop...")
        print("📺 Camera window should appear now!")
        
        while True:
            if not paused:
                ret, frame = cap.read()
                
                if not ret:
                    print("❌ Error: Could not read frame from camera")
                    break
                
                frame_count += 1
                
                # Detect faces and masks
                results = self.detect_faces_and_masks(frame)
                
                # Draw predictions
                frame_with_predictions = self.draw_predictions(frame, results)
                
                # Add info overlay
                info_text = f"Frame: {frame_count} | Faces: {len(results)} | Press 'q' to quit"
                cv2.putText(frame_with_predictions, info_text, (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Add model status
                model_status = "Demo Model (Untrained)" if not hasattr(self, 'trained_model') else "Trained Model"
                cv2.putText(frame_with_predictions, model_status, (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            
            # Display frame
            cv2.imshow('Face Mask Detection - Real Time', frame_with_predictions)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("👋 Quitting camera detection...")
                break
            elif key == ord('s'):
                screenshot_name = f"face_mask_detection_screenshot_{screenshot_count:03d}.jpg"
                cv2.imwrite(screenshot_name, frame_with_predictions)
                print(f"📸 Screenshot saved: {screenshot_name}")
                screenshot_count += 1
            elif key == ord(' '):  # Space bar
                paused = not paused
                print(f"⏸️  {'Paused' if paused else 'Resumed'}")
            elif key == ord('r'):
                frame_count = 0
                print("🔄 Reset frame counter")
        
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        print("✅ Camera detection stopped successfully")
    
    def test_with_image(self, image_path):
        """Test detection with a single image"""
        
        print(f"\n📷 TESTING WITH IMAGE: {image_path}")
        print("=" * 35)
        
        if not Path(image_path).exists():
            print(f"❌ Image not found: {image_path}")
            return
        
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            print(f"❌ Could not load image: {image_path}")
            return
        
        # Detect faces and masks
        results = self.detect_faces_and_masks(image)
        
        print(f"✅ Found {len(results)} faces")
        
        # Draw predictions
        result_image = self.draw_predictions(image.copy(), results)
        
        # Display results
        for i, result in enumerate(results):
            print(f"   Face {i+1}: {result['label']} ({result['confidence']:.2f})")
        
        # Save and show result
        output_path = f"test_result_{Path(image_path).stem}.jpg"
        cv2.imwrite(output_path, result_image)
        print(f"📁 Result saved: {output_path}")
        
        # Show image (optional)
        cv2.imshow('Face Mask Detection - Image Test', result_image)
        print("Press any key to close the image window...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def main():
    """Main function to run real-time face mask detection"""
    
    print("🎭 REAL-TIME FACE MASK DETECTION")
    print("=" * 34)
    
    # Initialize detector
    detector = RealTimeFaceMaskDetector()
    
    print("\n🎯 Choose an option:")
    print("1. 📹 Start real-time camera detection")
    print("2. 📷 Test with image file")
    print("3. 🔧 Camera troubleshooting")
    print("4. ❌ Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            # Camera detection
            camera_index = input("Enter camera index (default 0): ").strip()
            camera_index = int(camera_index) if camera_index.isdigit() else 0
            
            detector.start_camera_detection(camera_index)
            break
            
        elif choice == '2':
            # Image testing
            image_path = input("Enter image path: ").strip()
            if image_path:
                detector.test_with_image(image_path)
            break
            
        elif choice == '3':
            # Camera troubleshooting
            print("\n🔧 CAMERA TROUBLESHOOTING")
            print("=" * 24)
            
            print("📹 Available camera indices to try:")
            for i in range(5):
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        print(f"   ✅ Camera {i}: Working")
                    else:
                        print(f"   ⚠️  Camera {i}: Opens but no frames")
                    cap.release()
                else:
                    print(f"   ❌ Camera {i}: Not available")
            
            print("\n💡 Tips:")
            print("   - Try camera indices 0, 1, 2...")
            print("   - Check if other apps are using camera")
            print("   - Ensure camera permissions are granted")
            print("   - Try external USB camera if built-in fails")
            
        elif choice == '4':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()