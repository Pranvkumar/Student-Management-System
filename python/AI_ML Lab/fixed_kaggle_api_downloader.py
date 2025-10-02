#!/usr/bin/env python3
"""
Fixed Kaggle API Face Mask Dataset Downloader
=============================================
Properly handles Kaggle API imports and authentication
"""

import subprocess
import sys
import os
from pathlib import Path
import zipfile
import shutil

# Try to import kaggle API, handle if not available
try:
    import kaggle
    from kaggle.api.kaggle_api_extended import KaggleApi
    KAGGLE_API_AVAILABLE = True
except ImportError:
    KAGGLE_API_AVAILABLE = False
    kaggle = None
    KaggleApi = None

def ensure_kaggle_api_installed():
    """Ensure Kaggle API is installed and configured"""
    global KAGGLE_API_AVAILABLE, kaggle, KaggleApi
    
    if not KAGGLE_API_AVAILABLE:
        print("📦 Installing Kaggle API...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle"])
            
            # Try to import again after installation
            import kaggle
            from kaggle.api.kaggle_api_extended import KaggleApi
            KAGGLE_API_AVAILABLE = True
            
            print("✅ Kaggle API installed successfully")
        except Exception as e:
            print(f"❌ Failed to install Kaggle API: {e}")
            return False
    else:
        print("✅ Kaggle API already available")
    
    # Check for credentials
    return check_kaggle_credentials()

def check_kaggle_credentials():
    """Check if Kaggle credentials are properly configured"""
    
    print("\n🔑 CHECKING KAGGLE CREDENTIALS")
    print("=" * 32)
    
    # Check for kaggle.json in common locations
    kaggle_paths = [
        Path.home() / ".kaggle" / "kaggle.json",
        Path.cwd() / "kaggle.json",
    ]
    
    credentials_found = False
    for path in kaggle_paths:
        if path.exists():
            print(f"✅ Found credentials: {path}")
            credentials_found = True
            break
    
    if not credentials_found:
        print("❌ Kaggle credentials not found!")
        print("\n🔧 SETUP INSTRUCTIONS:")
        print("1. Go to https://www.kaggle.com/account")
        print("2. Click 'Create API Token'")
        print("3. Download kaggle.json file")
        print("4. Place in one of these locations:")
        for path in kaggle_paths:
            print(f"   📁 {path}")
        print("5. Set permissions (Linux/Mac): chmod 600 ~/.kaggle/kaggle.json")
        
        print("\n⚠️  Cannot proceed without Kaggle API credentials")
        return False
    
    # Test API connection
    try:
        api = KaggleApi()
        api.authenticate()
        print("✅ Kaggle API authentication successful")
        return True
    except Exception as e:
        print(f"❌ Kaggle API authentication failed: {e}")
        print("💡 Check your kaggle.json file format and permissions")
        return False

def download_with_kaggle_api():
    """Download face mask dataset using official Kaggle API"""
    
    if not KAGGLE_API_AVAILABLE:
        print("❌ Kaggle API not available")
        return None
    
    print("\n🎭 DOWNLOADING WITH KAGGLE API")
    print("=" * 32)
    
    try:
        # Initialize API
        api = KaggleApi()
        api.authenticate()
        
        dataset_name = "omkargurav/face-mask-dataset"
        download_dir = Path("Kaggle_API_Download")
        download_dir.mkdir(exist_ok=True)
        
        print(f"📥 Downloading {dataset_name}...")
        print(f"📁 Download directory: {download_dir}")
        
        # Download dataset
        api.dataset_download_files(
            dataset=dataset_name,
            path=str(download_dir),
            unzip=True
        )
        
        print("✅ Download completed successfully!")
        
        # List downloaded contents
        print(f"\n📂 Downloaded contents in {download_dir}:")
        items = list(download_dir.rglob("*"))
        
        dirs = [item for item in items if item.is_dir()]
        files = [item for item in items if item.is_file()]
        
        print(f"📁 Directories: {len(dirs)}")
        for directory in sorted(dirs):
            relative_path = directory.relative_to(download_dir)
            print(f"   📁 {relative_path}/")
        
        print(f"\n📄 Files: {len(files)}")
        for file in sorted(files)[:10]:  # Show first 10 files
            relative_path = file.relative_to(download_dir)
            size_mb = file.stat().st_size / (1024 * 1024) if file.stat().st_size > 0 else 0
            print(f"   📄 {relative_path} ({size_mb:.1f} MB)")
        
        if len(files) > 10:
            print(f"   ... and {len(files) - 10} more files")
        
        return str(download_dir)
        
    except Exception as e:
        print(f"❌ Download failed: {e}")
        print(f"Error type: {type(e).__name__}")
        
        if "403" in str(e) or "Forbidden" in str(e):
            print("💡 This might be an authentication issue")
            print("🔧 Try refreshing your Kaggle API token")
        elif "404" in str(e) or "Not Found" in str(e):
            print("💡 Dataset might not exist or be accessible")
            print(f"🔗 Check: https://www.kaggle.com/datasets/{dataset_name}")
        
        return None

def organize_kaggle_api_dataset(download_path):
    """Organize dataset downloaded via Kaggle API"""
    
    if not download_path or not Path(download_path).exists():
        print("❌ Invalid download path")
        return False
    
    print("\n🗂️  ORGANIZING KAGGLE API DATASET")
    print("=" * 34)
    
    source_path = Path(download_path)
    target_path = Path("Face_Mask_Dataset_KaggleAPI")
    
    # Create organized structure
    target_path.mkdir(exist_ok=True)
    (target_path / "with_mask").mkdir(exist_ok=True)
    (target_path / "without_mask").mkdir(exist_ok=True)
    (target_path / "original").mkdir(exist_ok=True)
    
    print(f"📁 Source: {source_path}")
    print(f"📁 Target: {target_path}")
    
    try:
        # Look for data directory or direct image folders
        data_sources = [
            source_path / "data",
            source_path,
        ]
        
        organized_count = 0
        
        for data_source in data_sources:
            if not data_source.exists():
                continue
            
            # Look for with_mask and without_mask folders
            with_mask_dir = data_source / "with_mask"
            without_mask_dir = data_source / "without_mask"
            
            if with_mask_dir.exists() and without_mask_dir.exists():
                print(f"📂 Found organized structure in: {data_source}")
                
                # Copy with_mask images
                with_mask_images = list(with_mask_dir.glob("*.*"))
                print(f"📊 Copying {len(with_mask_images)} masked images...")
                for img in with_mask_images:
                    if img.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
                        shutil.copy2(img, target_path / "with_mask" / img.name)
                        organized_count += 1
                
                # Copy without_mask images
                without_mask_images = list(without_mask_dir.glob("*.*"))
                print(f"📊 Copying {len(without_mask_images)} unmasked images...")
                for img in without_mask_images:
                    if img.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
                        shutil.copy2(img, target_path / "without_mask" / img.name)
                        organized_count += 1
                
                # Copy original structure
                shutil.copytree(data_source, target_path / "original" / "data", 
                               dirs_exist_ok=True)
                break
        
        if organized_count == 0:
            print("⚠️  No organized structure found, copying raw data")
            shutil.copytree(source_path, target_path / "original" / "raw", 
                           dirs_exist_ok=True)
            
            print("📋 Raw data copied to original/raw/")
            print("💡 Manual organization may be required")
            return True
        
        # Final statistics
        final_with_mask = len(list((target_path / "with_mask").glob("*.*")))
        final_without_mask = len(list((target_path / "without_mask").glob("*.*")))
        total_organized = final_with_mask + final_without_mask
        
        print(f"\n🎯 ORGANIZATION RESULTS:")
        print("=" * 25)
        print(f"📂 {target_path}/")
        print(f"├── with_mask/     ({final_with_mask:,} images)")
        print(f"├── without_mask/  ({final_without_mask:,} images)")
        print(f"└── original/      (backup)")
        
        print(f"\n📊 Total organized: {total_organized:,} images")
        
        if total_organized > 0:
            print("✅ Dataset ready for training!")
            
            # Create completion file
            completion_info = f"""
KAGGLE API DOWNLOAD SUCCESS
==========================

Download Method: Official Kaggle API
Dataset: omkargurav/face-mask-dataset
Status: ✅ COMPLETE

Organization Results:
- With Mask Images: {final_with_mask:,}
- Without Mask Images: {final_without_mask:,}
- Total Images: {total_organized:,}

Paths:
- Organized Dataset: {target_path}
- Original Download: {download_path}

Ready for machine learning training!

Next Steps:
1. Verify image quality in with_mask/ and without_mask/
2. Apply data augmentation during training
3. Train face mask detection model
4. Validate with test images

Generated by: Fixed Kaggle API Downloader
"""
            
            completion_file = target_path / "KAGGLE_API_SUCCESS.txt"
            with open(completion_file, 'w', encoding='utf-8') as f:
                f.write(completion_info)
            
            print(f"📋 Success report: {completion_file}")
            return True
        else:
            print("⚠️  Organization completed but no images found")
            return False
        
    except Exception as e:
        print(f"❌ Organization error: {e}")
        return False

def main():
    """Main execution with comprehensive error handling"""
    
    print("🚀 FIXED KAGGLE API FACE MASK DATASET DOWNLOADER")
    print("=" * 52)
    
    # Step 1: Setup Kaggle API
    print("\n1️⃣ Setting up Kaggle API...")
    if not ensure_kaggle_api_installed():
        print("\n❌ Cannot proceed without proper Kaggle API setup")
        print("\n🔧 QUICK SETUP GUIDE:")
        print("1. pip install kaggle")
        print("2. Get API token from https://www.kaggle.com/account")
        print("3. Place kaggle.json in ~/.kaggle/")
        print("4. Run this script again")
        return
    
    # Step 2: Download dataset
    print("\n2️⃣ Downloading face mask dataset...")
    download_path = download_with_kaggle_api()
    
    if not download_path:
        print("\n❌ Download failed")
        print("\n🔧 TROUBLESHOOTING:")
        print("1. Verify Kaggle API credentials")
        print("2. Check internet connection")
        print("3. Ensure dataset exists and is accessible")
        print("4. Try refreshing your API token")
        return
    
    # Step 3: Organize dataset
    print("\n3️⃣ Organizing dataset for machine learning...")
    if organize_kaggle_api_dataset(download_path):
        print("\n🎉 KAGGLE API DOWNLOAD SUCCESS!")
        print("=" * 35)
        print("\n✅ Face mask dataset downloaded and organized")
        print("✅ Ready for machine learning training")
        print("✅ All files properly structured")
        
        print("\n📁 Your dataset: Face_Mask_Dataset_KaggleAPI/")
        print("🚀 Start building your AI model!")
        
    else:
        print("\n⚠️  Download succeeded but organization needs manual work")
        print(f"📁 Raw data available: {download_path}")
        print("💡 Check downloaded files and organize manually if needed")

if __name__ == "__main__":
    main()