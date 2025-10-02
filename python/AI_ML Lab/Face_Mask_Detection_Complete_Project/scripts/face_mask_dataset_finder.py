#!/usr/bin/env python3
"""
Face Mask Dataset Finder and Downloader
=======================================
Comprehensive guide and automated downloader for face mask detection datasets
"""

import os
import requests
import zipfile
import urllib.request
from pathlib import Path
import json

class FaceMaskDatasetManager:
    def __init__(self, base_path="Face_Mask_Datasets"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        
    def print_available_datasets(self):
        """Print information about available face mask datasets"""
        print("🎭 FACE MASK DETECTION DATASETS")
        print("=" * 50)
        
        datasets = {
            "1. Face Mask Detection Dataset (12K Images)": {
                "source": "Kaggle",
                "url": "https://www.kaggle.com/datasets/omkargurav/face-mask-dataset",
                "size": "~109 MB",
                "images": "12,000+ images",
                "classes": "with_mask, without_mask",
                "description": "High-quality dataset with people wearing and not wearing masks"
            },
            
            "2. Medical Mask Dataset": {
                "source": "GitHub",
                "url": "https://github.com/cabani/MaskedFace-Net",
                "size": "~2 GB",
                "images": "137,016 images",
                "classes": "masked_faces, unmasked_faces",
                "description": "MaskedFace-Net dataset with realistic masked faces"
            },
            
            "3. Face Mask Detection Dataset (7K Images)": {
                "source": "Kaggle",
                "url": "https://www.kaggle.com/datasets/andrewmvd/face-mask-detection",
                "size": "~60 MB",
                "images": "7,000+ images",
                "classes": "with_mask, without_mask, mask_weared_incorrect",
                "description": "Dataset with 3 classes including incorrectly worn masks"
            },
            
            "4. Real-World Masked Face Dataset (RMFD)": {
                "source": "GitHub",
                "url": "https://github.com/X-zhangyang/Real-World-Masked-Face-Dataset",
                "size": "~500 MB",
                "images": "5,000+ images",
                "classes": "masked, unmasked",
                "description": "Real-world scenarios with various lighting and angles"
            },
            
            "5. COVID-19 Face Mask Detection Dataset": {
                "source": "Kaggle",
                "url": "https://www.kaggle.com/datasets/wobotintelligence/face-mask-detection-dataset",
                "size": "~200 MB",
                "images": "10,000+ images",
                "classes": "mask, no_mask",
                "description": "High-resolution images with bounding box annotations"
            }
        }
        
        for name, info in datasets.items():
            print(f"\n{name}")
            print(f"   📍 Source: {info['source']}")
            print(f"   🔗 URL: {info['url']}")
            print(f"   📦 Size: {info['size']}")
            print(f"   🖼️  Images: {info['images']}")
            print(f"   🏷️  Classes: {info['classes']}")
            print(f"   📝 Description: {info['description']}")
        
        return datasets
    
    def download_sample_dataset(self):
        """Download a small sample dataset for immediate use"""
        print("\n🚀 CREATING SAMPLE DATASET")
        print("=" * 30)
        
        # Create directory structure
        sample_dir = self.base_path / "sample_dataset"
        with_mask_dir = sample_dir / "with_mask"
        without_mask_dir = sample_dir / "without_mask"
        
        for directory in [sample_dir, with_mask_dir, without_mask_dir]:
            directory.mkdir(exist_ok=True)
        
        # Sample URLs (these are placeholder URLs - you would need actual image URLs)
        sample_urls = {
            "with_mask": [
                # Note: These are placeholder URLs. In practice, you'd use actual image URLs
                "https://example.com/mask1.jpg",
                "https://example.com/mask2.jpg",
            ],
            "without_mask": [
                "https://example.com/no_mask1.jpg",
                "https://example.com/no_mask2.jpg",
            ]
        }
        
        print("📁 Created directory structure:")
        print(f"   {sample_dir}")
        print(f"   ├── with_mask/")
        print(f"   └── without_mask/")
        
        # Create instructions file
        instructions = """
FACE MASK DATASET INSTRUCTIONS
=============================

To use this dataset structure:

1. MANUAL DOWNLOAD (Recommended):
   - Download from Kaggle: https://www.kaggle.com/datasets/omkargurav/face-mask-dataset
   - Extract to this folder
   - Organize images into with_mask/ and without_mask/ folders

2. WEB SCRAPING (Advanced):
   - Use the web scraper script to collect images
   - Ensure you have permission to use the images
   - Follow ethical guidelines for data collection

3. DIRECTORY STRUCTURE:
   Face_Mask_Datasets/
   ├── with_mask/          (Images of people wearing masks)
   ├── without_mask/       (Images of people not wearing masks)
   └── annotations/        (Optional: XML or JSON annotations)

4. IMAGE REQUIREMENTS:
   - Format: JPG, PNG
   - Resolution: 224x224 or higher
   - Quality: Good lighting, clear faces
   - Diversity: Different ages, ethnicities, angles

5. TRAINING TIPS:
   - Minimum 1000 images per class
   - 80/20 train/validation split
   - Data augmentation recommended
   - Balance classes for better performance
"""
        
        instructions_file = sample_dir / "README.txt"
        with open(instructions_file, 'w') as f:
            f.write(instructions)
        
        print(f"\n✅ Instructions saved to: {instructions_file}")
        return sample_dir
    
    def create_kaggle_download_script(self):
        """Create a script to download from Kaggle using Kaggle API"""
        script_content = '''#!/usr/bin/env python3
"""
Kaggle Dataset Downloader for Face Mask Detection
================================================
"""

import os
import subprocess
import sys

def install_kaggle():
    """Install kaggle API if not already installed"""
    try:
        import kaggle
        print("✅ Kaggle API already installed")
    except ImportError:
        print("📦 Installing Kaggle API...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle"])
        print("✅ Kaggle API installed successfully")

def setup_kaggle_credentials():
    """Guide user through Kaggle API setup"""
    print("\\n🔑 KAGGLE API SETUP")
    print("=" * 20)
    print("1. Go to https://www.kaggle.com/account")
    print("2. Click 'Create API Token'")
    print("3. Download kaggle.json file")
    print("4. Place kaggle.json in ~/.kaggle/ (Linux/Mac) or C:\\\\Users\\\\{username}\\\\.kaggle\\\\ (Windows)")
    print("5. Set permissions: chmod 600 ~/.kaggle/kaggle.json (Linux/Mac)")
    
    kaggle_dir = os.path.expanduser("~/.kaggle")
    kaggle_json = os.path.join(kaggle_dir, "kaggle.json")
    
    if os.path.exists(kaggle_json):
        print("✅ kaggle.json found!")
        return True
    else:
        print("❌ kaggle.json not found. Please set up Kaggle API credentials.")
        return False

def download_datasets():
    """Download face mask datasets from Kaggle"""
    datasets = [
        "omkargurav/face-mask-dataset",
        "andrewmvd/face-mask-detection",
        "wobotintelligence/face-mask-detection-dataset"
    ]
    
    for dataset in datasets:
        print(f"\\n📥 Downloading {dataset}...")
        try:
            subprocess.run(["kaggle", "datasets", "download", "-d", dataset], check=True)
            print(f"✅ Downloaded {dataset}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to download {dataset}")

def main():
    print("🎭 KAGGLE FACE MASK DATASET DOWNLOADER")
    print("=" * 45)
    
    # Install kaggle if needed
    install_kaggle()
    
    # Check credentials
    if setup_kaggle_credentials():
        download_datasets()
    else:
        print("\\n⚠️  Please set up Kaggle API credentials first")

if __name__ == "__main__":
    main()
'''
        
        script_file = self.base_path / "download_kaggle_datasets.py"
        with open(script_file, 'w') as f:
            f.write(script_content)
        
        print(f"\n📋 Kaggle download script created: {script_file}")
        return script_file
    
    def create_web_scraper(self):
        """Create a web scraper for collecting face mask images"""
        scraper_content = '''#!/usr/bin/env python3
"""
Face Mask Image Web Scraper
===========================
IMPORTANT: Use responsibly and respect website terms of service
"""

import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from pathlib import Path

class FaceMaskImageScraper:
    def __init__(self, download_dir="scraped_images"):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_and_download(self, query, max_images=100):
        """
        Search for images and download them
        Note: This is a template - actual implementation depends on specific sites
        """
        print(f"🔍 Searching for: {query}")
        print(f"📁 Download directory: {self.download_dir}")
        print(f"🎯 Max images: {max_images}")
        
        # Create subdirectory for this query
        query_dir = self.download_dir / query.replace(" ", "_")
        query_dir.mkdir(exist_ok=True)
        
        print("\\n⚠️  IMPORTANT NOTES:")
        print("   • Respect website terms of service")
        print("   • Don't overload servers with requests")
        print("   • Check image licenses and usage rights")
        print("   • Consider using public datasets instead")
        
        return query_dir

def main():
    print("🎭 FACE MASK IMAGE WEB SCRAPER")
    print("=" * 35)
    print("⚠️  Please use responsibly and ethically!")
    
    scraper = FaceMaskImageScraper()
    
    # Define search queries
    queries = [
        "people wearing face masks",
        "people without face masks",
        "medical masks coronavirus",
        "no mask faces"
    ]
    
    print("\\n📋 Recommended approach:")
    print("1. Use public datasets (Kaggle, GitHub)")
    print("2. If scraping, respect robots.txt")
    print("3. Check image licenses")
    print("4. Don't scrape copyrighted images")
    
    for query in queries:
        scraper.search_and_download(query, max_images=50)
        time.sleep(2)  # Be respectful to servers

if __name__ == "__main__":
    main()
'''
        
        scraper_file = self.base_path / "web_scraper.py"
        with open(scraper_file, 'w') as f:
            f.write(scraper_content)
        
        print(f"📋 Web scraper created: {scraper_file}")
        print("⚠️  Remember to use web scraping responsibly!")
        return scraper_file

def main():
    """Main execution function"""
    print("🎭 FACE MASK DATASET FINDER")
    print("=" * 30)
    
    # Initialize manager
    manager = FaceMaskDatasetManager()
    
    # Show available datasets
    datasets = manager.print_available_datasets()
    
    # Create sample dataset structure
    sample_dir = manager.download_sample_dataset()
    
    # Create download scripts
    kaggle_script = manager.create_kaggle_download_script()
    scraper_script = manager.create_web_scraper()
    
    print("\n🎉 DATASET SETUP COMPLETE!")
    print("=" * 25)
    print("\n📁 Created Files:")
    print(f"   📂 {manager.base_path}/")
    print(f"   ├── sample_dataset/")
    print(f"   ├── download_kaggle_datasets.py")
    print(f"   └── web_scraper.py")
    
    print("\n🚀 NEXT STEPS:")
    print("1. 📥 Download datasets from Kaggle (recommended)")
    print("2. 🏗️  Organize images in with_mask/ and without_mask/ folders")
    print("3. 🤖 Run your face mask detection training")
    
    print("\n💡 QUICK START:")
    print("   cd Face_Mask_Datasets")
    print("   python download_kaggle_datasets.py")

if __name__ == "__main__":
    main()