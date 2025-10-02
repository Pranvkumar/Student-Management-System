#!/usr/bin/env python3
"""
KaggleHub Face Mask Dataset Downloader
=====================================
Using KaggleHub to download face mask detection dataset
"""

import subprocess
import sys
import os
from pathlib import Path

def install_kagglehub():
    """Install KaggleHub if not already installed"""
    try:
        import kagglehub
        print("✅ KaggleHub already installed")
        return True
    except ImportError:
        print("📦 Installing KaggleHub...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "kagglehub"])
            print("✅ KaggleHub installed successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to install KaggleHub: {e}")
            return False

def download_face_mask_dataset():
    """Download face mask dataset using KaggleHub"""
    
    print("🎭 DOWNLOADING FACE MASK DATASET WITH KAGGLEHUB")
    print("=" * 55)
    
    try:
        # Import kagglehub
        import kagglehub
        
        # Download latest version
        print("📥 Downloading omkargurav/face-mask-dataset...")
        path = kagglehub.dataset_download("omkargurav/face-mask-dataset")
        
        print(f"✅ Download completed!")
        print(f"📁 Path to dataset files: {path}")
        
        # List contents of downloaded dataset
        dataset_path = Path(path)
        if dataset_path.exists():
            print("\n📂 Dataset Contents:")
            print("-" * 20)
            
            # List all files and directories
            items = list(dataset_path.rglob("*"))
            
            for item in sorted(items)[:20]:  # Show first 20 items
                relative_path = item.relative_to(dataset_path)
                if item.is_dir():
                    print(f"📁 {relative_path}/")
                else:
                    size = item.stat().st_size
                    size_mb = size / (1024 * 1024)
                    print(f"📄 {relative_path} ({size_mb:.1f} MB)")
            
            if len(items) > 20:
                print(f"... and {len(items) - 20} more items")
            
            # Count image files
            image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
            image_files = []
            
            for ext in image_extensions:
                image_files.extend(dataset_path.rglob(f"*{ext}"))
                image_files.extend(dataset_path.rglob(f"*{ext.upper()}"))
            
            print(f"\n📊 Found {len(image_files)} image files")
            
        return path
        
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        return None

def organize_dataset(download_path):
    """Organize the downloaded dataset"""
    
    if not download_path:
        return
    
    print("\n🗂️  ORGANIZING DATASET")
    print("=" * 22)
    
    source_path = Path(download_path)
    target_path = Path("Face_Mask_Dataset_Downloaded")
    
    # Create target directory
    target_path.mkdir(exist_ok=True)
    
    print(f"📁 Source: {source_path}")
    print(f"📁 Target: {target_path}")
    
    # Copy organized structure
    try:
        import shutil
        
        # Create subdirectories
        (target_path / "with_mask").mkdir(exist_ok=True)
        (target_path / "without_mask").mkdir(exist_ok=True)
        (target_path / "original").mkdir(exist_ok=True)
        
        # Copy original dataset
        if source_path.exists():
            print("📋 Copying dataset files...")
            
            # Copy entire dataset to original folder
            for item in source_path.iterdir():
                if item.is_file():
                    shutil.copy2(item, target_path / "original")
                elif item.is_dir():
                    shutil.copytree(item, target_path / "original" / item.name, 
                                  dirs_exist_ok=True)
            
            print("✅ Dataset copied to Face_Mask_Dataset_Downloaded/")
            
        # Create instructions
        instructions = f"""
KAGGLEHUB DATASET DOWNLOADED
===========================

Original Dataset Path: {download_path}
Organized Dataset Path: {target_path}

NEXT STEPS:
1. Check Face_Mask_Dataset_Downloaded/original/ for raw data
2. Organize images into:
   - Face_Mask_Dataset_Downloaded/with_mask/
   - Face_Mask_Dataset_Downloaded/without_mask/
3. Run your face mask detection training

DATASET INFO:
- Source: omkargurav/face-mask-dataset
- Downloaded via: KaggleHub API
- Date: {Path(__file__).stat().st_mtime if Path(__file__).exists() else 'Unknown'}
"""
        
        instructions_file = target_path / "DATASET_INFO.txt"
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"📋 Instructions saved to: {instructions_file}")
        
    except Exception as e:
        print(f"⚠️  Organization error: {e}")
        print("💡 You can manually organize the dataset from the download path")

def main():
    """Main execution function"""
    
    print("🚀 KAGGLEHUB FACE MASK DATASET DOWNLOADER")
    print("=" * 45)
    
    # Install KaggleHub
    if not install_kagglehub():
        print("❌ Cannot proceed without KaggleHub")
        return
    
    # Download dataset
    download_path = download_face_mask_dataset()
    
    if download_path:
        # Organize dataset
        organize_dataset(download_path)
        
        print("\n🎉 DOWNLOAD AND SETUP COMPLETE!")
        print("=" * 35)
        print("\n✅ Dataset successfully downloaded!")
        print(f"📁 Original location: {download_path}")
        print("📁 Organized location: Face_Mask_Dataset_Downloaded/")
        
        print("\n🚀 Next Steps:")
        print("1. Organize images in with_mask/ and without_mask/ folders")
        print("2. Train your face mask detection model")
        print("3. Test with real images or webcam")
        
    else:
        print("\n❌ Download failed. Please check your internet connection")
        print("💡 Alternative: Download manually from Kaggle website")

if __name__ == "__main__":
    main()