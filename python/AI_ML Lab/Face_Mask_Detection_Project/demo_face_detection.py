#!/usr/bin/env python3
"""
Face Mask Detection Demo
========================

A simple demo script to test the face mask detection system.
This script provides quick testing without the full interactive menu.
"""

import cv2
import os
import sys

# Add the current directory to path to import our module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from face_mask_detection import FaceMaskDetector
except ImportError:
    print("❌ Could not import FaceMaskDetector. Make sure face_mask_detection.py is in the same directory.")
    sys.exit(1)

def demo_webcam():
    """Quick webcam demo"""
    print("🎥 Starting webcam demo...")
    detector = FaceMaskDetector()
    detector.load_face_detector_dnn()
    
    # Try to load pre-trained model (optional)
    detector.load_mask_detector()
    
    detector.run_webcam_detection()

def demo_face_detection_only():
    """Demo with face detection only (no mask classification)"""
    print("👤 Face detection demo (no mask detection)")
    
    detector = FaceMaskDetector()
    detector.load_face_detector_dnn()
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Could not open webcam")
        return
    
    print("Press 'q' to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect faces only
        faces = detector.detect_faces_dnn(frame) if detector.face_net else detector.detect_faces_haar(frame)
        
        # Draw face rectangles
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Face Detected", (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Show face count
        cv2.putText(frame, f"Faces: {len(faces)}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Press 'q' to quit", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.imshow('Face Detection Demo', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def demo_image_test():
    """Demo with a test image"""
    print("🖼️  Image detection demo")
    
    # Create a simple test pattern if no image is available
    import numpy as np
    
    # Create a test image
    test_image = np.zeros((400, 400, 3), dtype=np.uint8)
    cv2.putText(test_image, "No test image available", (50, 200), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(test_image, "Use your own image", (100, 240), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    cv2.imshow("Test Image - Press any key to continue", test_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("💡 To test with real images:")
    print("   1. Save an image file (jpg, png, etc.)")
    print("   2. Use: detector.detect_from_image('path/to/image.jpg')")

def main():
    """Main demo function"""
    print("🎭 Face Mask Detection System - Quick Demo")
    print("=" * 50)
    
    # Check if required libraries are available
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow version: {tf.__version__}")
    except ImportError:
        print("⚠️  TensorFlow not installed. Install with: pip install tensorflow")
    
    try:
        import cv2
        print(f"✅ OpenCV version: {cv2.__version__}")
    except ImportError:
        print("❌ OpenCV not installed. Install with: pip install opencv-python")
        return
    
    print("\n🎯 Choose a demo:")
    print("1. 👤 Face detection only (works without trained model)")
    print("2. 🎥 Full webcam demo (face + mask detection)")
    print("3. 🖼️  Image test demo")
    print("4. 📚 Show system info")
    print("5. ❌ Exit")
    
    while True:
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            demo_face_detection_only()
            break
        elif choice == '2':
            demo_webcam()
            break
        elif choice == '3':
            demo_image_test()
            break
        elif choice == '4':
            show_system_info()
            break
        elif choice == '5':
            print("👋 Demo ended!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-5.")

def show_system_info():
    """Show system information"""
    print("\n🔍 System Information:")
    print("-" * 30)
    
    # Python version
    import sys
    print(f"🐍 Python: {sys.version}")
    
    # Check webcam
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print("📹 Webcam: Available")
        cap.release()
    else:
        print("📹 Webcam: Not available")
    
    # Check GPU
    try:
        import tensorflow as tf
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"🚀 GPU: {len(gpus)} device(s) available")
        else:
            print("🚀 GPU: Not available (using CPU)")
    except:
        print("🚀 GPU: Cannot detect")
    
    # File structure
    current_dir = os.getcwd()
    print(f"📁 Current directory: {current_dir}")
    
    files = [
        "face_mask_detection.py",
        "requirements_face_detection.txt", 
        "README_Face_Detection.md"
    ]
    
    print("📋 Project files:")
    for file in files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (missing)")

if __name__ == "__main__":
    main()