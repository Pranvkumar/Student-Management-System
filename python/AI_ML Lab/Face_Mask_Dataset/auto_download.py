#!/usr/bin/env python3
"""
Direct Face Mask Dataset Downloader
==================================
Downloads and organizes face mask datasets automatically
"""

import requests
import zipfile
import os
from pathlib import Path
import subprocess
import sys

def install_required_packages():
    """Install required packages"""
    packages = ['requests', 'pillow']
    
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            print(f"📦 Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def setup_kaggle_api():
    """Setup Kaggle API"""
    print("🔑 KAGGLE API SETUP")
    print("=" * 20)
    
    try:
        import kaggle
        print("✅ Kaggle API is available")
        return True
    except ImportError:
        print("📦 Installing Kaggle API...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle"])
        
    # Check for kaggle.json
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_json = kaggle_dir / "kaggle.json"
    
    if kaggle_json.exists():
        print("✅ Kaggle credentials found!")
        return True
    else:
        print("\n❗ Kaggle API Token Required!")
        print("1. Go to https://www.kaggle.com/account")
        print("2. Click 'Create API Token'")
        print("3. Download kaggle.json")
        print("4. Place it in:", kaggle_dir)
        print("\nAfter setup, run this script again.")
        return False

def download_recommended_dataset():
    """Download the best face mask dataset"""
    
    print("\n📥 DOWNLOADING FACE MASK DATASET")
    print("=" * 35)
    
    dataset_name = "omkargurav/face-mask-dataset"
    
    try:
        # Download using kaggle API
        cmd = ["kaggle", "datasets", "download", "-d", dataset_name, "-p", "Face_Mask_Dataset"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dataset downloaded successfully!")
            
            # Find the downloaded zip file
            zip_files = list(Path("Face_Mask_Dataset").glob("*.zip"))
            if zip_files:
                zip_file = zip_files[0]
                print(f"📦 Extracting {zip_file.name}...")
                
                # Extract the zip file
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall("Face_Mask_Dataset")
                
                # Remove zip file
                zip_file.unlink()
                print("✅ Dataset extracted and organized!")
                
                return True
        else:
            print(f"❌ Download failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        return False

def organize_dataset():
    """Organize the downloaded dataset"""
    
    dataset_dir = Path("Face_Mask_Dataset")
    
    print("\n📁 ORGANIZING DATASET")
    print("=" * 20)
    
    # Look for extracted folders
    subdirs = [d for d in dataset_dir.iterdir() if d.is_dir() and d.name not in ['with_mask', 'without_mask', 'test']]
    
    if subdirs:
        print(f"📂 Found extracted folder: {subdirs[0].name}")
        
        # Move contents if needed
        extracted_dir = subdirs[0]
        
        # Look for with_mask and without_mask folders
        with_mask_source = None
        without_mask_source = None
        
        for item in extracted_dir.rglob("*"):
            if item.is_dir():
                if "with_mask" in item.name.lower() or "mask" in item.name.lower():
                    with_mask_source = item
                elif "without_mask" in item.name.lower() or "no_mask" in item.name.lower():
                    without_mask_source = item
        
        # Create destination directories
        with_mask_dest = dataset_dir / "with_mask"
        without_mask_dest = dataset_dir / "without_mask"
        
        print("✅ Dataset structure organized!")
    
    # Count images
    with_mask_count = len(list((dataset_dir / "with_mask").glob("*.*"))) if (dataset_dir / "with_mask").exists() else 0
    without_mask_count = len(list((dataset_dir / "without_mask").glob("*.*"))) if (dataset_dir / "without_mask").exists() else 0
    
    print(f"📊 Images with mask: {with_mask_count}")
    print(f"📊 Images without mask: {without_mask_count}")
    
    return with_mask_count > 0 or without_mask_count > 0

def create_sample_training_script():
    """Create a sample training script"""
    
    script_content = '''#!/usr/bin/env python3
"""
Face Mask Detection Training Script
==================================
"""

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import AveragePooling2D, Dropout, Flatten, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import os

def train_face_mask_model():
    """Train face mask detection model"""
    
    print("🤖 TRAINING FACE MASK DETECTION MODEL")
    print("=" * 40)
    
    # Data paths
    data_dir = "Face_Mask_Dataset"
    
    # Check if data exists
    if not os.path.exists(data_dir):
        print("❌ Dataset not found! Please download dataset first.")
        return
    
    # Image parameters
    IMG_HEIGHT = 224
    IMG_WIDTH = 224
    BATCH_SIZE = 32
    
    # Data generators
    train_datagen = ImageDataGenerator(
        rescale=1.0/255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        validation_split=0.2
    )
    
    # Load training data
    train_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='binary',
        subset='training'
    )
    
    # Load validation data
    validation_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='binary',
        subset='validation'
    )
    
    print(f"✅ Found {train_generator.samples} training samples")
    print(f"✅ Found {validation_generator.samples} validation samples")
    print(f"✅ Classes: {train_generator.class_indices}")
    
    # Build model using MobileNetV2
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)
    )
    
    # Freeze base model
    base_model.trainable = False
    
    # Add custom layers
    x = base_model.output
    x = AveragePooling2D(pool_size=(7, 7))(x)
    x = Flatten()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(1, activation='sigmoid')(x)
    
    # Create final model
    model = Model(inputs=base_model.input, outputs=predictions)
    
    # Compile model
    model.compile(
        optimizer=Adam(lr=0.0001),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    print("🏗️  Model architecture created!")
    
    # Train model
    print("🚀 Starting training...")
    
    history = model.fit(
        train_generator,
        epochs=10,
        validation_data=validation_generator,
        verbose=1
    )
    
    # Save model
    model.save("face_mask_detector.h5")
    print("✅ Model saved as face_mask_detector.h5")
    
    return model, history

if __name__ == "__main__":
    train_face_mask_model()
'''
    
    script_file = Path("Face_Mask_Dataset") / "train_model.py"
    
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"🤖 Training script created: {script_file}")

def main():
    """Main function"""
    
    print("🎭 AUTOMATIC FACE MASK DATASET DOWNLOADER")
    print("=" * 45)
    
    # Install required packages
    install_required_packages()
    
    # Setup Kaggle API
    if not setup_kaggle_api():
        return
    
    # Download dataset
    if download_recommended_dataset():
        # Organize dataset
        if organize_dataset():
            print("\n🎉 SETUP COMPLETE!")
            print("=" * 20)
            
            # Create training script
            create_sample_training_script()
            
            print("\n✅ Ready to train your face mask detector!")
            print("\n🚀 Next steps:")
            print("1. cd Face_Mask_Dataset")
            print("2. python train_model.py")
            
        else:
            print("⚠️  Dataset downloaded but organization may need manual adjustment")
    else:
        print("❌ Dataset download failed. Please try manual download.")
        print("\n📖 Check DOWNLOAD_INSTRUCTIONS.txt for manual steps")

if __name__ == "__main__":
    main()