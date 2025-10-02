#!/usr/bin/env python3
"""
Face Mask Detection System - Setup Script
==========================================

This script helps you set up the Face Mask Detection system by:
1. Installing required packages
2. Testing system components
3. Creating sample dataset structure
4. Running initial tests
"""

import subprocess
import sys
import os

def install_packages():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    packages = [
        "tensorflow>=2.8.0",
        "opencv-python>=4.6.0", 
        "scikit-learn>=1.1.0",
        "numpy>=1.21.0",
        "matplotlib>=3.5.0",
        "Pillow>=8.3.0"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    
    return True

def test_imports():
    """Test if all required modules can be imported"""
    print("\n🧪 Testing imports...")
    
    modules = {
        'tensorflow': 'TensorFlow',
        'cv2': 'OpenCV',
        'sklearn': 'Scikit-learn', 
        'numpy': 'NumPy',
        'matplotlib': 'Matplotlib',
        'PIL': 'Pillow'
    }
    
    success = True
    for module, name in modules.items():
        try:
            __import__(module)
            print(f"✅ {name} imported successfully")
        except ImportError:
            print(f"❌ {name} import failed")
            success = False
    
    return success

def check_webcam():
    """Check if webcam is available"""
    print("\n📹 Checking webcam...")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Webcam is available")
            cap.release()
            return True
        else:
            print("❌ Webcam is not available")
            return False
    except Exception as e:
        print(f"❌ Error checking webcam: {e}")
        return False

def create_project_structure():
    """Create project directory structure"""
    print("\n📁 Creating project structure...")
    
    directories = [
        "dataset/with_mask",
        "dataset/without_mask", 
        "models",
        "test_images",
        "results"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}/")
    
    # Create sample info file
    with open("dataset/README.txt", "w") as f:
        f.write("""Face Mask Dataset Structure
===========================

with_mask/     - Put images of people wearing masks here
without_mask/  - Put images of people without masks here

Recommended:
- At least 100 images per category
- Various lighting conditions
- Different face angles
- Mixed demographics
- Clear face visibility

Supported formats: .jpg, .jpeg, .png, .bmp
""")
    
    print("✅ Project structure created")

def download_sample_models():
    """Download or create sample model files"""
    print("\n🤖 Setting up model files...")
    
    # Create a simple model info file
    with open("models/model_info.txt", "w") as f:
        f.write("""Model Information
================

To use the face mask detection system:

1. For face detection:
   - Haar Cascade: Built into OpenCV
   - DNN Model: Optional, better accuracy

2. For mask detection:
   - Train your own model using the dataset
   - Or use pre-trained models

Training command:
python face_mask_detection.py
> Choose option 3 (Train new model)

Model files will be saved as:
- mask_detector.model (trained model)
- lb.pickle (label binarizer)
""")
    
    print("✅ Model info created")

def run_basic_test():
    """Run a basic system test"""
    print("\n🔬 Running basic system test...")
    
    try:
        # Test OpenCV
        import cv2
        print("✅ OpenCV test passed")
        
        # Test TensorFlow
        import tensorflow as tf
        print(f"✅ TensorFlow {tf.__version__} test passed")
        
        # Test face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        if face_cascade.empty():
            print("❌ Face cascade not loaded")
            return False
        else:
            print("✅ Face detection test passed")
        
        print("✅ All basic tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Basic test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🎭 Face Mask Detection System Setup")
    print("=" * 40)
    
    print("This setup will:")
    print("1. Install required Python packages")
    print("2. Test system components")  
    print("3. Create project structure")
    print("4. Run basic functionality tests")
    
    proceed = input("\n🚀 Do you want to proceed? (y/n): ")
    if proceed.lower() != 'y':
        print("Setup cancelled.")
        return
    
    # Step 1: Install packages
    if not install_packages():
        print("❌ Package installation failed. Please install manually.")
        return
    
    # Step 2: Test imports
    if not test_imports():
        print("❌ Import tests failed. Some packages may not be installed correctly.")
        return
    
    # Step 3: Check webcam
    check_webcam()
    
    # Step 4: Create structure
    create_project_structure()
    
    # Step 5: Setup models
    download_sample_models()
    
    # Step 6: Basic test
    if run_basic_test():
        print("\n🎉 Setup completed successfully!")
        print("\n📚 Next steps:")
        print("1. Add training images to dataset/with_mask/ and dataset/without_mask/")
        print("2. Run: python face_mask_detection.py")
        print("3. Or run quick demo: python demo_face_detection.py")
        print("\n📖 Read README_Face_Detection.md for detailed instructions")
    else:
        print("\n⚠️  Setup completed with warnings. Check error messages above.")

if __name__ == "__main__":
    main()