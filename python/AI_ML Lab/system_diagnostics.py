#!/usr/bin/env python3
"""
Face Mask Detection - System Diagnostics
========================================
Quick system check and troubleshooting tool
"""

import os
import sys
from pathlib import Path

def main():
    print("🔧 FACE MASK DETECTION - SYSTEM DIAGNOSTICS")
    print("=" * 50)
    
    # Check Python version
    print(f"📍 Python Version: {sys.version}")
    print(f"📍 Python Path: {sys.executable}")
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"📍 Current Directory: {current_dir}")
    
    # Check for required files
    print("\n📁 FILE CHECK:")
    print("-" * 20)
    
    required_files = [
        "launch_camera_interface.py",
        "clean_camera_interface.py", 
        "modern_camera_interface.py",
        "camera_mask_detection.py",
        "face_mask_detector_ready.h5"
    ]
    
    for file in required_files:
        if Path(file).exists():
            file_size = Path(file).stat().st_size / 1024
            print(f"✅ {file} ({file_size:.1f} KB)")
        else:
            print(f"❌ {file} - NOT FOUND")
    
    # Check dependencies
    print("\n📦 DEPENDENCY CHECK:")
    print("-" * 25)
    
    dependencies = [
        ("opencv-python", "cv2"),
        ("numpy", "numpy"),
        ("tensorflow", "tensorflow"),
        ("pillow", "PIL")
    ]
    
    for package_name, import_name in dependencies:
        try:
            module = __import__(import_name)
            version = getattr(module, '__version__', 'Unknown')
            print(f"✅ {package_name}: {version}")
        except ImportError:
            print(f"❌ {package_name}: NOT INSTALLED")
    
    # Camera test
    print("\n📹 CAMERA TEST:")
    print("-" * 15)
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                h, w, c = frame.shape
                print(f"✅ Camera working: {w}x{h} resolution, {c} channels")
                
                # Test face detection
                face_cascade = cv2.CascadeClassifier(
                    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
                )
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray)
                print(f"✅ Face detection: {len(faces)} faces detected in test frame")
                
            else:
                print("⚠️  Camera detected but no frame received")
            
            cap.release()
        else:
            print("❌ Cannot access camera (may be in use by another app)")
            
    except Exception as e:
        print(f"❌ Camera test failed: {e}")
    
    # AI Model test
    print("\n🤖 AI MODEL TEST:")
    print("-" * 20)
    
    try:
        import tensorflow as tf
        tf.get_logger().setLevel('ERROR')  # Suppress logs
        
        model_found = False
        for path in ["face_mask_detector_ready.h5", "Face_Mask_Detection_Complete_Project/face_mask_detector_ready.h5"]:
            if Path(path).exists():
                try:
                    model = tf.keras.models.load_model(path, compile=False)
                    print(f"✅ Model loaded: {path}")
                    print(f"   Input shape: {model.input_shape}")
                    print(f"   Output shape: {model.output_shape}")
                    model_found = True
                    break
                except Exception as e:
                    print(f"⚠️  Model file exists but failed to load: {e}")
        
        if not model_found:
            print("❌ No working AI model found")
            print("   System will work in face detection only mode")
            
    except ImportError:
        print("❌ TensorFlow not available - AI predictions disabled")
    except Exception as e:
        print(f"❌ Model test failed: {e}")
    
    # Quick fix suggestions
    print("\n🛠️  QUICK FIXES:")
    print("-" * 15)
    print("1. Install missing packages:")
    print("   pip install opencv-python numpy tensorflow pillow")
    print()
    print("2. If camera not working:")
    print("   - Close other applications using camera")
    print("   - Check camera permissions")
    print("   - Try different camera index (change 0 to 1 in code)")
    print()
    print("3. If AI model not found:")
    print("   - Ensure face_mask_detector_ready.h5 is in this directory")
    print("   - Check Face_Mask_Detection_Complete_Project folder")
    print()
    print("4. Run interfaces directly:")
    print(f"   {sys.executable} clean_camera_interface.py")
    print(f"   {sys.executable} modern_camera_interface.py")
    
    print(f"\n📍 To run with current Python: {sys.executable} <script_name>")
    print("✅ Diagnostics complete!")

if __name__ == "__main__":
    main()