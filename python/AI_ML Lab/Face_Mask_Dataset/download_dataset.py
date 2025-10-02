#!/usr/bin/env python3
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
    
    print("\nChoose dataset to download:")
    print("1. Face Mask Dataset (12K images) - Recommended")
    print("2. Face Mask Detection (7K images, 3 classes)")
    print("3. COVID-19 Face Mask Dataset (10K images)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice in datasets:
        dataset_name = datasets[choice]
        print(f"\n📥 Downloading {dataset_name}...")
        download_dataset(dataset_name)
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
