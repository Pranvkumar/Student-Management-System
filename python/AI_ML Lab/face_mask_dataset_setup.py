#!/usr/bin/env python3
"""
Face Mask Dataset Guide and Downloader
=====================================
Simple guide to find and download face mask datasets
"""

import os
from pathlib import Path

def create_dataset_structure():
    """Create proper directory structure for face mask dataset"""
    
    print("🎭 FACE MASK DATASET SETUP")
    print("=" * 30)
    
    # Create main dataset directory
    dataset_dir = Path("Face_Mask_Dataset")
    dataset_dir.mkdir(exist_ok=True)
    
    # Create subdirectories
    with_mask_dir = dataset_dir / "with_mask"
    without_mask_dir = dataset_dir / "without_mask"
    test_dir = dataset_dir / "test"
    
    for directory in [with_mask_dir, without_mask_dir, test_dir]:
        directory.mkdir(exist_ok=True)
    
    print("📁 Created directory structure:")
    print(f"   {dataset_dir}/")
    print(f"   ├── with_mask/      (Put masked face images here)")
    print(f"   ├── without_mask/   (Put unmasked face images here)")
    print(f"   └── test/           (Put test images here)")
    
    return dataset_dir

def create_download_instructions():
    """Create detailed download instructions"""
    
    instructions = """
FACE MASK DATASET DOWNLOAD GUIDE
===============================

TOP 5 RECOMMENDED DATASETS:

1. Face Mask Detection Dataset (12K Images) - BEST FOR BEGINNERS
   URL: https://www.kaggle.com/datasets/omkargurav/face-mask-dataset
   Size: 109 MB
   Images: 12,000+ high-quality images
   Classes: with_mask, without_mask
   
2. Face Mask Detection Dataset (7K Images) - 3-CLASS VERSION
   URL: https://www.kaggle.com/datasets/andrewmvd/face-mask-detection
   Size: 60 MB
   Images: 7,000+ images
   Classes: with_mask, without_mask, mask_weared_incorrect
   
3. COVID-19 Face Mask Detection Dataset
   URL: https://www.kaggle.com/datasets/wobotintelligence/face-mask-detection-dataset
   Size: 200 MB
   Images: 10,000+ images with bounding boxes
   
4. MaskedFace-Net (Large Dataset)
   URL: https://github.com/cabani/MaskedFace-Net
   Size: 2 GB
   Images: 137,016 images
   Note: Very large, use if you need maximum data
   
5. Real-World Masked Face Dataset (RMFD)
   URL: https://github.com/X-zhangyang/Real-World-Masked-Face-Dataset
   Size: 500 MB
   Images: 5,000+ real-world scenarios

DOWNLOAD STEPS:

METHOD 1 - KAGGLE (RECOMMENDED):
1. Go to https://www.kaggle.com/
2. Create free account
3. Search for "face mask detection"
4. Download dataset ZIP file
5. Extract to Face_Mask_Dataset/ folder
6. Organize images into with_mask/ and without_mask/ folders

METHOD 2 - KAGGLE API:
1. pip install kaggle
2. Go to Kaggle Account > Create API Token
3. Download kaggle.json to ~/.kaggle/
4. Run: kaggle datasets download -d omkargurav/face-mask-dataset
5. Extract and organize

METHOD 3 - GITHUB:
1. Visit GitHub repository links above
2. Clone or download ZIP
3. Follow repository instructions
4. Organize data as needed

QUICK START COMMANDS:
pip install kaggle
kaggle datasets download -d omkargurav/face-mask-dataset
unzip face-mask-dataset.zip -d Face_Mask_Dataset/

DATA ORGANIZATION TIPS:
- Minimum 1000 images per class
- Balance classes (same number of masked/unmasked)
- Use 80% for training, 20% for validation
- Ensure image quality (clear faces, good lighting)
- Various angles, ages, ethnicities for better generalization

NEXT STEPS AFTER DOWNLOAD:
1. Organize images in correct folders
2. Run data preprocessing
3. Train your face mask detection model
4. Test on real images/webcam
"""
    
    # Save instructions to file
    instructions_file = Path("Face_Mask_Dataset") / "DOWNLOAD_INSTRUCTIONS.txt"
    
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"📋 Instructions saved to: {instructions_file}")
    return instructions_file

def create_kaggle_downloader():
    """Create simple Kaggle downloader script"""
    
    kaggle_script = '''# Face Mask Dataset Kaggle Downloader
# Run these commands in your terminal:

# 1. Install Kaggle API
pip install kaggle

# 2. Download datasets (choose one):

# Option A: 12K Images Dataset (Recommended for beginners)
kaggle datasets download -d omkargurav/face-mask-dataset

# Option B: 7K Images with 3 classes
kaggle datasets download -d andrewmvd/face-mask-detection

# Option C: COVID-19 Dataset with bounding boxes
kaggle datasets download -d wobotintelligence/face-mask-detection-dataset

# 3. Extract downloaded file
# Windows: Use WinRAR/7-Zip or Python zipfile
# Linux/Mac: unzip filename.zip -d Face_Mask_Dataset/

# 4. Organize data structure:
# Face_Mask_Dataset/
#   ├── with_mask/
#   ├── without_mask/
#   └── test/
'''
    
    script_file = Path("Face_Mask_Dataset") / "kaggle_download_commands.txt"
    
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(kaggle_script)
    
    print(f"📥 Kaggle commands saved to: {script_file}")
    return script_file

def create_python_downloader():
    """Create Python script to help with dataset downloading"""
    
    python_script = '''#!/usr/bin/env python3
"""
Face Mask Dataset Python Helper
==============================
"""

import subprocess
import sys
import os
from pathlib import Path

def install_kaggle():
    """Install Kaggle API"""
    try:
        import kaggle
        print("✅ Kaggle API already installed")
        return True
    except ImportError:
        print("📦 Installing Kaggle API...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle"])
        print("✅ Kaggle API installed")
        return True

def download_dataset(dataset_name):
    """Download dataset from Kaggle"""
    try:
        cmd = ["kaggle", "datasets", "download", "-d", dataset_name]
        subprocess.run(cmd, check=True)
        print(f"✅ Downloaded {dataset_name}")
        return True
    except Exception as e:
        print(f"❌ Failed to download {dataset_name}: {e}")
        return False

def main():
    print("🎭 Face Mask Dataset Downloader")
    print("=" * 35)
    
    # Install kaggle
    if not install_kaggle():
        return
    
    # Available datasets
    datasets = {
        "1": "omkargurav/face-mask-dataset",
        "2": "andrewmvd/face-mask-detection",
        "3": "wobotintelligence/face-mask-detection-dataset"
    }
    
    print("\\nChoose dataset to download:")
    print("1. Face Mask Dataset (12K images) - Recommended")
    print("2. Face Mask Detection (7K images, 3 classes)")
    print("3. COVID-19 Face Mask Dataset (10K images)")
    
    choice = input("\\nEnter choice (1-3): ").strip()
    
    if choice in datasets:
        dataset_name = datasets[choice]
        print(f"\\n📥 Downloading {dataset_name}...")
        download_dataset(dataset_name)
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
'''
    
    python_file = Path("Face_Mask_Dataset") / "download_dataset.py"
    
    with open(python_file, 'w', encoding='utf-8') as f:
        f.write(python_script)
    
    print(f"🐍 Python downloader saved to: {python_file}")
    return python_file

def main():
    """Main function"""
    print("🎯 SETTING UP FACE MASK DATASET")
    print("=" * 35)
    
    # Create directory structure
    dataset_dir = create_dataset_structure()
    
    # Create download instructions
    instructions_file = create_download_instructions()
    
    # Create download helpers
    kaggle_file = create_kaggle_downloader()
    python_file = create_python_downloader()
    
    print("\n🎉 SETUP COMPLETE!")
    print("=" * 20)
    print("\n📁 Created Files:")
    print(f"   📂 {dataset_dir}/")
    print(f"   ├── with_mask/")
    print(f"   ├── without_mask/") 
    print(f"   ├── test/")
    print(f"   ├── DOWNLOAD_INSTRUCTIONS.txt")
    print(f"   ├── kaggle_download_commands.txt")
    print(f"   └── download_dataset.py")
    
    print("\n🚀 NEXT STEPS:")
    print("1. 📖 Read DOWNLOAD_INSTRUCTIONS.txt")
    print("2. 📥 Download dataset from Kaggle")
    print("3. 📁 Extract and organize images")
    print("4. 🤖 Train your face mask detection model")
    
    print("\n💡 RECOMMENDED DATASET:")
    print("   🎯 Face Mask Dataset (12K Images)")
    print("   🔗 https://www.kaggle.com/datasets/omkargurav/face-mask-dataset")
    print("   📦 Size: 109 MB (perfect for beginners)")

if __name__ == "__main__":
    main()