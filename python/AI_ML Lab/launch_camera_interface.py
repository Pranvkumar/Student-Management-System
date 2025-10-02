#!/usr/bin/env python3
"""
Face Mask Detection Interface Launcher
=====================================
Choose between different camera interface styles
"""

import os
import sys
from pathlib import Path

def check_dependencies():
    """Check if required packages are available"""
    try:
        import cv2
        import numpy as np
        cv2_version = cv2.__version__
    except ImportError:
        print("❌ OpenCV not found. Install with: pip install opencv-python")
        return False
    
    try:
        import tensorflow as tf
        tf_available = True
        tf_version = tf.__version__
    except ImportError:
        tf_available = False
        tf_version = "Not installed"
    
    print("📦 DEPENDENCIES CHECK:")
    print(f"   ✅ OpenCV: {cv2_version}")
    print(f"   {'✅' if tf_available else '⚠️ '} TensorFlow: {tf_version}")
    if not tf_available:
        print("      Note: AI predictions will be disabled without TensorFlow")
    
    return True

def show_interface_menu():
    """Display interface selection menu"""
    print("\n🎭 FACE MASK DETECTION - INTERFACE SELECTOR")
    print("=" * 50)
    print("Choose your preferred camera interface style:")
    print()
    print("1. 🎯 Original Interface    - Full-featured with detailed info")
    print("2. 🎨 Clean Interface      - Minimal and distraction-free") 
    print("3. ✨ Modern Interface     - Sleek with animations and stats")
    print("4. 📊 Check System Info    - View dependencies and model status")
    print("5. ❌ Exit")
    print()
    
    while True:
        try:
            choice = input("Enter your choice (1-5): ").strip()
            if choice in ['1', '2', '3', '4', '5']:
                return choice
            else:
                print("⚠️  Please enter a number between 1-5")
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            return '5'

def check_model_status():
    """Check if trained model is available"""
    model_paths = [
        "face_mask_detector_ready.h5",
        "Face_Mask_Detection_Complete_Project/face_mask_detector_ready.h5",
        "../face_mask_detector_ready.h5",
        "Face_Mask_Detection_Complete_Project/models/face_mask_detector_ready.h5"
    ]
    
    print("\n🔍 MODEL STATUS CHECK:")
    print("-" * 25)
    
    for path in model_paths:
        if Path(path).exists():
            file_size = Path(path).stat().st_size / (1024 * 1024)  # MB
            print(f"✅ Found: {path} ({file_size:.1f} MB)")
            return True
        else:
            print(f"❌ Not found: {path}")
    
    print("\n⚠️  No trained model found!")
    print("   The system will work in face detection mode only.")
    print("   To enable AI mask detection, ensure the model file is available.")
    return False

def launch_interface(choice):
    """Launch the selected interface"""
    if choice == '1':
        print("\n🚀 Launching Original Interface...")
        try:
            from camera_mask_detection import main
            main()
        except ImportError:
            print("❌ Original interface file not found: camera_mask_detection.py")
        except Exception as e:
            print(f"❌ Error launching original interface: {e}")
            
    elif choice == '2':
        print("\n🚀 Launching Clean Interface...")
        try:
            from clean_camera_interface import main
            main()
        except ImportError:
            print("❌ Clean interface file not found: clean_camera_interface.py")
        except Exception as e:
            print(f"❌ Error launching clean interface: {e}")
            
    elif choice == '3':
        print("\n🚀 Launching Modern Interface...")
        try:
            from modern_camera_interface import main
            main()
        except ImportError:
            print("❌ Modern interface file not found: modern_camera_interface.py")
        except Exception as e:
            print(f"❌ Error launching modern interface: {e}")
            
    elif choice == '4':
        print("\n📊 SYSTEM INFORMATION:")
        print("=" * 30)
        check_dependencies()
        check_model_status()
        
        # Camera check
        print("\n📹 CAMERA CHECK:")
        print("-" * 15)
        try:
            import cv2
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    h, w = frame.shape[:2]
                    print(f"✅ Camera working: {w}x{h} resolution")
                else:
                    print("⚠️  Camera detected but no frame received")
                cap.release()
            else:
                print("❌ Cannot access camera")
        except Exception as e:
            print(f"❌ Camera check failed: {e}")
        
        input("\nPress Enter to continue...")
        return False  # Return to menu
        
    elif choice == '5':
        print("\n👋 Thanks for using Face Mask Detection!")
        return True
    
    return True

def main():
    """Main launcher function"""
    print("🎭 Face Mask Detection System")
    print("Version 2.0 - Clean Interface Edition")
    
    # Check system
    if not check_dependencies():
        input("\nPress Enter to exit...")
        return
    
    # Main menu loop
    while True:
        choice = show_interface_menu()
        
        if launch_interface(choice):
            break  # Exit if user chose to quit or interface completed
    
    print("✨ Face Mask Detection System closed.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 System interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your Python environment and try again.")