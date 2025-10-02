#!/usr/bin/env python3
"""
Quick Face Mask Model Training
===============================
Fast training for camera testing
"""

import os
import cv2
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

def quick_train_model():
    """Quick training of face mask detection model"""
    
    print("🚀 QUICK FACE MASK MODEL TRAINING")
    print("=" * 35)
    
    try:
        import tensorflow as tf
        from tensorflow.keras.applications import MobileNetV2
        from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
        from tensorflow.keras.models import Model
        from tensorflow.keras.optimizers import Adam
        from tensorflow.keras.preprocessing.image import ImageDataGenerator
        print("✅ TensorFlow loaded successfully")
    except ImportError as e:
        print(f"❌ TensorFlow not available: {e}")
        return False
    
    # Find dataset
    dataset_paths = [
        "Face_Mask_Detection_Complete_Project/datasets",
        "Face_Mask_Dataset",
        "Face_Mask_Datasets", 
        "Face_Mask_Dataset_Downloaded"
    ]
    
    dataset_dir = None
    for path in dataset_paths:
        if Path(path).exists():
            # Look for mask/no_mask or with_mask/without_mask subdirectories
            potential_dirs = []
            for subdir in Path(path).iterdir():
                if subdir.is_dir():
                    potential_dirs.extend([
                        subdir / "with_mask",
                        subdir / "without_mask", 
                        subdir / "mask",
                        subdir / "no_mask",
                        subdir / "Mask",
                        subdir / "NoMask"
                    ])
            
            # Check if any of these exist and have images
            for pdir in potential_dirs:
                if pdir.exists():
                    image_files = list(pdir.glob("*.jpg")) + list(pdir.glob("*.png")) + list(pdir.glob("*.jpeg"))
                    if len(image_files) > 0:
                        dataset_dir = pdir.parent
                        print(f"✅ Found dataset: {dataset_dir}")
                        break
            
            if dataset_dir:
                break
    
    if not dataset_dir:
        print("❌ No dataset found!")
        print("💡 Available directories:")
        for path in dataset_paths:
            if Path(path).exists():
                print(f"   - {path}")
                for subdir in Path(path).iterdir():
                    if subdir.is_dir():
                        print(f"     └── {subdir.name}")
        return False
    
    print(f"📂 Using dataset: {dataset_dir}")
    
    # Check dataset structure
    subdirs = [d for d in Path(dataset_dir).iterdir() if d.is_dir()]
    print(f"📁 Found {len(subdirs)} categories:")
    for subdir in subdirs:
        image_count = len(list(subdir.glob("*.jpg")) + list(subdir.glob("*.png")) + list(subdir.glob("*.jpeg")))
        print(f"   - {subdir.name}: {image_count} images")
    
    if len(subdirs) != 2:
        print("❌ Expected exactly 2 categories (mask/no_mask)")
        return False
    
    # Create data generators
    print("\n🔄 Setting up data generators...")
    
    IMG_SIZE = 224
    BATCH_SIZE = 32
    
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1.0/255.0,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        validation_split=0.2
    )
    
    # Training generator
    train_generator = train_datagen.flow_from_directory(
        dataset_dir,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='binary',
        subset='training'
    )
    
    # Validation generator
    validation_generator = train_datagen.flow_from_directory(
        dataset_dir,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='binary',
        subset='validation'
    )
    
    print(f"✅ Training samples: {train_generator.samples}")
    print(f"✅ Validation samples: {validation_generator.samples}")
    print(f"✅ Class indices: {train_generator.class_indices}")
    
    # Create model
    print("\n🏗️  Building model...")
    
    # Load pre-trained MobileNetV2
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=(IMG_SIZE, IMG_SIZE, 3)
    )
    
    # Freeze base model
    base_model.trainable = False
    
    # Add custom head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    predictions = Dense(1, activation='sigmoid')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    
    # Compile model
    model.compile(
        optimizer=Adam(learning_rate=0.0001),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    print(f"✅ Model created with {model.count_params():,} parameters")
    
    # Train model (quick training - just 5 epochs)
    print("\n🎯 Training model (5 epochs for quick results)...")
    
    history = model.fit(
        train_generator,
        epochs=5,
        validation_data=validation_generator,
        verbose=1
    )
    
    # Save model
    model_path = "face_mask_detector_quick.h5"
    model.save(model_path)
    print(f"✅ Model saved as: {model_path}")
    
    # Create a simple plot
    try:
        plt.figure(figsize=(12, 4))
        
        plt.subplot(1, 2, 1)
        plt.plot(history.history['loss'], label='Training Loss')
        plt.plot(history.history['val_loss'], label='Validation Loss')
        plt.title('Model Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        
        plt.subplot(1, 2, 2)
        plt.plot(history.history['accuracy'], label='Training Accuracy')
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
        plt.title('Model Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()
        
        plot_path = "quick_training_history.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Training plot saved as: {plot_path}")
    except Exception as e:
        print(f"⚠️  Could not save plot: {e}")
    
    # Final accuracy
    final_acc = history.history['val_accuracy'][-1]
    print(f"\n🎯 Final Validation Accuracy: {final_acc:.4f} ({final_acc*100:.2f}%)")
    
    return True

if __name__ == "__main__":
    try:
        success = quick_train_model()
        if success:
            print("\n✅ Quick training completed!")
            print("🎥 Now you can test with camera using the trained model")
        else:
            print("\n❌ Training failed")
    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        import traceback
        traceback.print_exc()