#!/usr/bin/env python3
"""
Fix Dataset Structure and Train Model
====================================
Clean up dataset and train model
"""

import os
import shutil
from pathlib import Path

def fix_dataset_structure():
    """Fix the dataset structure for training"""
    
    print("🔧 FIXING DATASET STRUCTURE")
    print("=" * 30)
    
    # Source dataset
    source_dir = Path("Face_Mask_Detection_Complete_Project/datasets/kagglehub_dataset")
    
    # Create clean dataset directory
    clean_dir = Path("clean_face_mask_dataset")
    
    if clean_dir.exists():
        print("🗑️  Removing existing clean dataset...")
        shutil.rmtree(clean_dir)
    
    clean_dir.mkdir(exist_ok=True)
    
    # Create category directories
    mask_dir = clean_dir / "mask"
    no_mask_dir = clean_dir / "no_mask"
    
    mask_dir.mkdir(exist_ok=True)
    no_mask_dir.mkdir(exist_ok=True)
    
    print(f"📁 Created clean dataset structure:")
    print(f"   - {mask_dir}")
    print(f"   - {no_mask_dir}")
    
    # Copy files
    with_mask_source = source_dir / "with_mask"
    without_mask_source = source_dir / "without_mask"
    
    print("\n📋 Copying files...")
    
    # Copy with_mask images
    if with_mask_source.exists():
        mask_files = list(with_mask_source.glob("*.jpg")) + list(with_mask_source.glob("*.png")) + list(with_mask_source.glob("*.jpeg"))
        print(f"📸 Copying {len(mask_files)} mask images...")
        for i, img_file in enumerate(mask_files[:1000]):  # Limit to 1000 for quick training
            dest_file = mask_dir / f"mask_{i:04d}.jpg"
            shutil.copy2(img_file, dest_file)
    
    # Copy without_mask images  
    if without_mask_source.exists():
        no_mask_files = list(without_mask_source.glob("*.jpg")) + list(without_mask_source.glob("*.png")) + list(without_mask_source.glob("*.jpeg"))
        print(f"📸 Copying {len(no_mask_files)} no-mask images...")
        for i, img_file in enumerate(no_mask_files[:1000]):  # Limit to 1000 for quick training
            dest_file = no_mask_dir / f"no_mask_{i:04d}.jpg"
            shutil.copy2(img_file, dest_file)
    
    # Verify structure
    mask_count = len(list(mask_dir.glob("*")))
    no_mask_count = len(list(no_mask_dir.glob("*")))
    
    print(f"\n✅ Clean dataset created:")
    print(f"   - Mask images: {mask_count}")
    print(f"   - No-mask images: {no_mask_count}")
    print(f"   - Total: {mask_count + no_mask_count}")
    
    return clean_dir if mask_count > 0 and no_mask_count > 0 else None

def train_model_with_clean_data(dataset_dir):
    """Train model with clean dataset"""
    
    print(f"\n🚀 TRAINING MODEL WITH CLEAN DATA")
    print("=" * 35)
    
    try:
        import tensorflow as tf
        from tensorflow.keras.applications import MobileNetV2
        from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
        from tensorflow.keras.models import Model
        from tensorflow.keras.optimizers import Adam
        from tensorflow.keras.preprocessing.image import ImageDataGenerator
        print("✅ TensorFlow ready")
    except ImportError as e:
        print(f"❌ TensorFlow not available: {e}")
        return False
    
    print(f"📂 Using dataset: {dataset_dir}")
    
    # Setup data generators
    IMG_SIZE = 224
    BATCH_SIZE = 16  # Smaller batch for quick training
    
    # Data augmentation
    train_datagen = ImageDataGenerator(
        rescale=1.0/255.0,
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
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
    
    print(f"🎯 Training samples: {train_generator.samples}")
    print(f"🎯 Validation samples: {validation_generator.samples}")
    print(f"🎯 Classes: {train_generator.class_indices}")
    
    # Create model
    print("\n🏗️  Building MobileNetV2 model...")
    
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=(IMG_SIZE, IMG_SIZE, 3)
    )
    
    base_model.trainable = False
    
    # Add classification head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    predictions = Dense(1, activation='sigmoid')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    
    # Compile
    model.compile(
        optimizer=Adam(learning_rate=0.0001),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    print(f"✅ Model ready: {model.count_params():,} parameters")
    
    # Train for quick results
    print("\n🎯 Training (3 epochs for quick testing)...")
    
    history = model.fit(
        train_generator,
        epochs=3,
        validation_data=validation_generator,
        verbose=1
    )
    
    # Save model
    model_path = "face_mask_detector_ready.h5"
    model.save(model_path)
    print(f"✅ Model saved: {model_path}")
    
    # Final results
    final_acc = history.history['val_accuracy'][-1]
    final_loss = history.history['val_loss'][-1]
    
    print(f"\n🎯 FINAL RESULTS:")
    print(f"   - Validation Accuracy: {final_acc:.4f} ({final_acc*100:.2f}%)")
    print(f"   - Validation Loss: {final_loss:.4f}")
    
    return True

if __name__ == "__main__":
    try:
        print("🎭 FACE MASK MODEL TRAINING PIPELINE")
        print("=" * 40)
        
        # Step 1: Fix dataset structure
        clean_dataset = fix_dataset_structure()
        
        if clean_dataset is None:
            print("❌ Could not create clean dataset")
            exit(1)
        
        # Step 2: Train model
        success = train_model_with_clean_data(clean_dataset)
        
        if success:
            print("\n🎉 SUCCESS! Model ready for camera testing!")
            print("🎥 Run the camera detection script to test")
        else:
            print("\n❌ Training failed")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()