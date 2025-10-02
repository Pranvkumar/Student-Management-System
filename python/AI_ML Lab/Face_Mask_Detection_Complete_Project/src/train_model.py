#!/usr/bin/env python3
"""
Train Face Mask Detection Model
==============================
Train a face mask detection model using your dataset
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def check_dependencies():
    """Check if all required packages are available"""
    
    print("🔍 CHECKING DEPENDENCIES")
    print("=" * 26)
    
    required_packages = {
        'tensorflow': 'TensorFlow for deep learning',
        'cv2': 'OpenCV for computer vision',
        'sklearn': 'Scikit-learn for ML utilities',
        'matplotlib': 'Matplotlib for plotting',
        'numpy': 'NumPy for numerical computing'
    }
    
    missing_packages = []
    
    for package, description in required_packages.items():
        try:
            if package == 'cv2':
                import cv2
                print(f"✅ OpenCV: {cv2.__version__}")
            elif package == 'tensorflow':
                import tensorflow as tf
                print(f"✅ TensorFlow: {tf.__version__}")
            elif package == 'sklearn':
                import sklearn
                print(f"✅ Scikit-learn: {sklearn.__version__}")
            elif package == 'matplotlib':
                import matplotlib
                print(f"✅ Matplotlib: {matplotlib.__version__}")
            elif package == 'numpy':
                import numpy as np
                print(f"✅ NumPy: {np.__version__}")
                
        except ImportError:
            print(f"❌ {package}: NOT FOUND")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("💡 Install with: pip install tensorflow opencv-python scikit-learn matplotlib numpy")
        return False
    
    print("\n✅ All dependencies available!")
    return True

def find_dataset():
    """Find the face mask dataset"""
    
    print("\n📁 FINDING DATASET")
    print("=" * 18)
    
    # Look for dataset in common locations
    possible_paths = [
        Path("../datasets/kagglehub_dataset/with_mask"),
        Path("../datasets/kagglehub_dataset/original/data"),
        Path("datasets/kagglehub_dataset/with_mask"),
        Path("datasets/kagglehub_dataset/original/data"),
        Path("Face_Mask_Dataset_Downloaded/with_mask"),
        Path("../Face_Mask_Dataset_Downloaded/with_mask"),
    ]
    
    dataset_path = None
    
    for path in possible_paths:
        if path.exists():
            # Check if it has the right structure
            parent_dir = path.parent
            with_mask_dir = parent_dir / "with_mask"
            without_mask_dir = parent_dir / "without_mask"
            
            if with_mask_dir.exists() and without_mask_dir.exists():
                with_mask_count = len(list(with_mask_dir.glob("*.jpg")))
                without_mask_count = len(list(without_mask_dir.glob("*.jpg")))
                
                if with_mask_count > 0 and without_mask_count > 0:
                    dataset_path = parent_dir
                    print(f"✅ Found dataset: {dataset_path}")
                    print(f"   📊 With mask: {with_mask_count} images")
                    print(f"   📊 Without mask: {without_mask_count} images")
                    break
    
    if not dataset_path:
        print("❌ No suitable dataset found!")
        print("💡 Expected structure:")
        print("   dataset_folder/")
        print("   ├── with_mask/     (JPG images)")
        print("   └── without_mask/  (JPG images)")
        return None
    
    return dataset_path

def create_and_train_model(dataset_path):
    """Create and train the face mask detection model"""
    
    print("\n🤖 CREATING AND TRAINING MODEL")
    print("=" * 32)
    
    try:
        import tensorflow as tf
        from tensorflow.keras.preprocessing.image import ImageDataGenerator
        from tensorflow.keras.applications import MobileNetV2
        from tensorflow.keras.layers import AveragePooling2D, Dropout, Flatten, Dense, Input
        from tensorflow.keras.models import Model
        from tensorflow.keras.optimizers import Adam
        from sklearn.model_selection import train_test_split
        
        print("✅ Imports successful")
        
        # Parameters
        IMG_HEIGHT = 224
        IMG_WIDTH = 224
        BATCH_SIZE = 32
        EPOCHS = 10
        
        print(f"📊 Training parameters:")
        print(f"   - Image size: {IMG_WIDTH}x{IMG_HEIGHT}")
        print(f"   - Batch size: {BATCH_SIZE}")
        print(f"   - Epochs: {EPOCHS}")
        
        # Create data generators
        print("\n📁 Setting up data generators...")
        
        train_datagen = ImageDataGenerator(
            rescale=1.0/255.0,
            rotation_range=20,
            zoom_range=0.15,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.15,
            horizontal_flip=True,
            fill_mode="nearest",
            validation_split=0.2
        )
        
        # Training generator
        train_generator = train_datagen.flow_from_directory(
            str(dataset_path),
            target_size=(IMG_HEIGHT, IMG_WIDTH),
            batch_size=BATCH_SIZE,
            class_mode="binary",
            subset="training"
        )
        
        # Validation generator
        validation_generator = train_datagen.flow_from_directory(
            str(dataset_path),
            target_size=(IMG_HEIGHT, IMG_WIDTH),
            batch_size=BATCH_SIZE,
            class_mode="binary",
            subset="validation"
        )
        
        print(f"✅ Data generators created")
        print(f"   📊 Training samples: {train_generator.samples}")
        print(f"   📊 Validation samples: {validation_generator.samples}")
        print(f"   🏷️  Classes: {train_generator.class_indices}")
        
        # Create model
        print("\n🏗️  Building model architecture...")
        
        # Load pre-trained MobileNetV2
        base_model = MobileNetV2(
            weights="imagenet",
            include_top=False,
            input_tensor=Input(shape=(IMG_HEIGHT, IMG_WIDTH, 3))
        )
        
        # Freeze base model
        base_model.trainable = False
        
        # Add custom head
        head_model = base_model.output
        head_model = AveragePooling2D(pool_size=(7, 7))(head_model)
        head_model = Flatten(name="flatten")(head_model)
        head_model = Dense(128, activation="relu")(head_model)
        head_model = Dropout(0.5)(head_model)
        head_model = Dense(1, activation="sigmoid")(head_model)
        
        # Create final model
        model = Model(inputs=base_model.input, outputs=head_model)
        
        print("✅ Model architecture created")
        
        # Compile model
        print("⚙️  Compiling model...")
        
        model.compile(
            loss="binary_crossentropy",
            optimizer=Adam(learning_rate=1e-4),
            metrics=["accuracy"]
        )
        
        print("✅ Model compiled")
        
        # Display model summary
        print("\n📋 Model Summary:")
        model.summary()
        
        # Train model
        print(f"\n🚀 Starting training for {EPOCHS} epochs...")
        print("⏳ This may take several minutes...")
        
        history = model.fit(
            train_generator,
            steps_per_epoch=train_generator.samples // BATCH_SIZE,
            validation_data=validation_generator,
            validation_steps=validation_generator.samples // BATCH_SIZE,
            epochs=EPOCHS,
            verbose=1
        )
        
        print("✅ Training completed!")
        
        # Save model
        model_path = "face_mask_detector_trained.h5"
        model.save(model_path)
        print(f"💾 Model saved: {model_path}")
        
        # Plot training history
        print("\n📊 Plotting training history...")
        plot_training_history(history)
        
        # Evaluate model
        print("\n📈 Final Evaluation:")
        val_loss, val_accuracy = model.evaluate(validation_generator, verbose=0)
        print(f"   📊 Validation Accuracy: {val_accuracy:.4f}")
        print(f"   📊 Validation Loss: {val_loss:.4f}")
        
        return model_path
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Install missing packages: pip install tensorflow opencv-python")
        return None
    except Exception as e:
        print(f"❌ Training error: {e}")
        return None

def plot_training_history(history):
    """Plot training accuracy and loss"""
    
    try:
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(12, 4))
        
        # Plot accuracy
        plt.subplot(1, 2, 1)
        plt.plot(history.history['accuracy'], label='Training Accuracy')
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
        plt.title('Model Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()
        
        # Plot loss
        plt.subplot(1, 2, 2)
        plt.plot(history.history['loss'], label='Training Loss')
        plt.plot(history.history['val_loss'], label='Validation Loss')
        plt.title('Model Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        
        plt.tight_layout()
        
        # Save plot
        plot_path = "training_history.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"📊 Training history plot saved: {plot_path}")
        
        # Show plot
        plt.show()
        
    except Exception as e:
        print(f"⚠️  Could not create plot: {e}")

def main():
    """Main training function"""
    
    print("🤖 FACE MASK DETECTION MODEL TRAINER")
    print("=" * 38)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Cannot proceed without required packages")
        print("🔧 Install with:")
        print("   pip install tensorflow opencv-python scikit-learn matplotlib numpy")
        return
    
    # Find dataset
    dataset_path = find_dataset()
    if not dataset_path:
        print("\n❌ Cannot proceed without dataset")
        print("💡 Make sure your dataset is organized with with_mask/ and without_mask/ folders")
        return
    
    # Train model
    print("\n🎯 Ready to start training!")
    proceed = input("Continue with training? (y/n): ").lower().strip()
    
    if proceed == 'y':
        model_path = create_and_train_model(dataset_path)
        
        if model_path:
            print(f"\n🎉 TRAINING COMPLETE!")
            print("=" * 20)
            print(f"✅ Model saved: {model_path}")
            print("✅ Training history plotted")
            print("✅ Ready for real-time detection!")
            
            print(f"\n🚀 Next steps:")
            print(f"1. Run camera detection: python real_time_camera_detection.py")
            print(f"2. Use your trained model: {model_path}")
            print(f"3. Test with images or webcam")
        else:
            print("\n❌ Training failed")
            print("💡 Check error messages above")
    else:
        print("👋 Training cancelled")

if __name__ == "__main__":
    main()