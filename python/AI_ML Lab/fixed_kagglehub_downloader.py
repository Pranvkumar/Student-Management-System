#!/usr/bin/env python3
"""
Fixed KaggleHub Face Mask Dataset Downloader
===========================================
Properly handles imports and downloads face mask datasets
"""

import subprocess
import sys
import os
from pathlib import Path
import shutil

# Try to import kagglehub, install if needed
try:
    import kagglehub
    KAGGLEHUB_AVAILABLE = True
except ImportError:
    KAGGLEHUB_AVAILABLE = False

def ensure_kagglehub_installed():
    """Ensure KaggleHub is installed"""
    global KAGGLEHUB_AVAILABLE
    
    if KAGGLEHUB_AVAILABLE:
        print("✅ KaggleHub already available")
        return True
    
    print("📦 Installing KaggleHub...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "kagglehub"])
        
        # Try to import again after installation
        global kagglehub
        import kagglehub
        KAGGLEHUB_AVAILABLE = True
        
        print("✅ KaggleHub installed and imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to install KaggleHub: {e}")
        return False

def download_face_mask_dataset():
    """Download face mask dataset using KaggleHub"""
    
    if not KAGGLEHUB_AVAILABLE:
        print("❌ KaggleHub not available")
        return None
    
    print("🎭 DOWNLOADING FACE MASK DATASET WITH KAGGLEHUB")
    print("=" * 55)
    
    try:
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
            
            # Show directory structure
            dirs = [item for item in items if item.is_dir()]
            files = [item for item in items if item.is_file()]
            
            print(f"📁 Directories found: {len(dirs)}")
            for directory in sorted(dirs)[:10]:  # Show first 10 directories
                relative_path = directory.relative_to(dataset_path)
                print(f"   📁 {relative_path}/")
            
            print(f"\n📄 Files found: {len(files)}")
            
            # Count image files
            image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
            image_files = []
            
            for ext in image_extensions:
                image_files.extend(dataset_path.rglob(f"*{ext}"))
                image_files.extend(dataset_path.rglob(f"*{ext.upper()}"))
            
            print(f"🖼️  Image files: {len(image_files)}")
            
            # Show sample file names
            if image_files:
                print("\n📋 Sample image files:")
                for img in sorted(image_files)[:5]:
                    relative_path = img.relative_to(dataset_path)
                    size_mb = img.stat().st_size / (1024 * 1024)
                    print(f"   📄 {relative_path} ({size_mb:.1f} MB)")
        
        return str(path)
        
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {str(e)}")
        return None

def organize_downloaded_dataset(download_path):
    """Organize the downloaded dataset into proper structure"""
    
    if not download_path or not Path(download_path).exists():
        print("❌ Invalid download path")
        return False
    
    print("\n🗂️  ORGANIZING DATASET")
    print("=" * 22)
    
    source_path = Path(download_path)
    target_path = Path("Face_Mask_Dataset_KaggleHub")
    
    # Create target directory structure
    target_path.mkdir(exist_ok=True)
    (target_path / "with_mask").mkdir(exist_ok=True)
    (target_path / "without_mask").mkdir(exist_ok=True)
    (target_path / "original").mkdir(exist_ok=True)
    
    print(f"📁 Source: {source_path}")
    print(f"📁 Target: {target_path}")
    
    try:
        # Look for the data directory structure
        data_dir = None
        
        # Check common patterns
        possible_data_dirs = [
            source_path / "data",
            source_path,
        ]
        
        for possible_dir in possible_data_dirs:
            if possible_dir.exists():
                with_mask_dir = possible_dir / "with_mask"
                without_mask_dir = possible_dir / "without_mask"
                
                if with_mask_dir.exists() and without_mask_dir.exists():
                    data_dir = possible_dir
                    break
        
        if not data_dir:
            print("⚠️  Standard data directory structure not found")
            print("📁 Available directories:")
            for item in source_path.iterdir():
                if item.is_dir():
                    print(f"   📁 {item.name}")
            
            # Copy everything to original for manual organization
            shutil.copytree(source_path, target_path / "original" / "raw_data", 
                          dirs_exist_ok=True)
            print("📋 Copied raw data to original/raw_data/ for manual organization")
            return True
        
        # Organize with_mask images
        with_mask_source = data_dir / "with_mask"
        if with_mask_source.exists():
            with_mask_images = list(with_mask_source.glob("*.jpg")) + list(with_mask_source.glob("*.png"))
            print(f"📊 Found {len(with_mask_images)} images with masks")
            
            for img in with_mask_images:
                shutil.copy2(img, target_path / "with_mask" / img.name)
            
            print(f"✅ Copied {len(with_mask_images)} masked images")
        
        # Organize without_mask images
        without_mask_source = data_dir / "without_mask"
        if without_mask_source.exists():
            without_mask_images = list(without_mask_source.glob("*.jpg")) + list(without_mask_source.glob("*.png"))
            print(f"📊 Found {len(without_mask_images)} images without masks")
            
            for img in without_mask_images:
                shutil.copy2(img, target_path / "without_mask" / img.name)
            
            print(f"✅ Copied {len(without_mask_images)} unmasked images")
        
        # Copy original data as backup
        shutil.copytree(data_dir, target_path / "original" / "data", 
                       dirs_exist_ok=True)
        
        # Final count
        final_with_mask = len(list((target_path / "with_mask").glob("*.*")))
        final_without_mask = len(list((target_path / "without_mask").glob("*.*")))
        
        print(f"\n🎯 ORGANIZATION COMPLETE:")
        print("=" * 25)
        print(f"📂 {target_path}/")
        print(f"├── with_mask/     ({final_with_mask:,} images)")
        print(f"├── without_mask/  ({final_without_mask:,} images)")
        print(f"└── original/      (backup data)")
        
        total_images = final_with_mask + final_without_mask
        print(f"\n📊 Total organized: {total_images:,} images")
        
        if total_images > 0:
            print("✅ Dataset ready for face mask detection training!")
            
            # Create success file
            success_info = f"""
KAGGLEHUB DOWNLOAD SUCCESS
=========================

Download Details:
- Source: omkargurav/face-mask-dataset
- Method: KaggleHub API
- Original Path: {download_path}
- Organized Path: {target_path}

Dataset Statistics:
- With Mask: {final_with_mask:,} images
- Without Mask: {final_without_mask:,} images
- Total: {total_images:,} images

Status: ✅ READY FOR TRAINING

Next Steps:
1. Use with_mask/ and without_mask/ folders for training
2. Apply data augmentation
3. Train face mask detection model
4. Test with real images/webcam

Generated: {Path(__file__).stat().st_mtime if Path(__file__).exists() else 'Unknown'}
"""
            
            success_file = target_path / "KAGGLEHUB_SUCCESS.txt"
            with open(success_file, 'w', encoding='utf-8') as f:
                f.write(success_info)
            
            print(f"📋 Success details saved: {success_file}")
            return True
        else:
            print("⚠️  No images were organized")
            return False
        
    except Exception as e:
        print(f"❌ Organization error: {e}")
        return False

def main():
    """Main execution function with proper error handling"""
    
    print("🚀 FIXED KAGGLEHUB FACE MASK DATASET DOWNLOADER")
    print("=" * 50)
    
    # Step 1: Ensure KaggleHub is installed
    print("\n1️⃣ Checking KaggleHub installation...")
    if not ensure_kagglehub_installed():
        print("❌ Cannot proceed without KaggleHub")
        print("💡 Try installing manually: pip install kagglehub")
        return
    
    # Step 2: Download dataset
    print("\n2️⃣ Downloading face mask dataset...")
    download_path = download_face_mask_dataset()
    
    if not download_path:
        print("❌ Download failed")
        print("\n🔧 Troubleshooting:")
        print("1. Check internet connection")
        print("2. Verify Kaggle access (no login required for public datasets)")
        print("3. Try manual download from Kaggle website")
        return
    
    # Step 3: Organize dataset
    print("\n3️⃣ Organizing dataset...")
    if organize_downloaded_dataset(download_path):
        print("\n🎉 SUCCESS! FACE MASK DATASET READY!")
        print("=" * 40)
        print("\n✅ KaggleHub download completed successfully")
        print("✅ Dataset organized for machine learning")
        print("✅ Ready for face mask detection training")
        
        print("\n📁 Your dataset is in: Face_Mask_Dataset_KaggleHub/")
        print("🚀 Start training your AI model now!")
        
    else:
        print("\n⚠️  Download succeeded but organization needs attention")
        print(f"📁 Raw data available at: {download_path}")
        print("💡 Check Face_Mask_Dataset_KaggleHub/original/ for manual organization")

if __name__ == "__main__":
    main()