import cv2
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import os
import pickle

class FaceMaskDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.mask_detector = None
        self.face_net = None
        self.confidence_threshold = 0.5
        
    def load_face_detector_dnn(self):
        """Load pre-trained DNN face detection model"""
        try:
            # Load the DNN model for better face detection
            net = cv2.dnn.readNetFromTensorflow('opencv_face_detector_uint8.pb', 
                                              'opencv_face_detector.pbtxt')
            self.face_net = net
            print("✅ DNN Face detector loaded successfully")
        except:
            print("⚠️  DNN model not found, using Haar Cascade instead")
            self.face_net = None
    
    def detect_faces_dnn(self, frame):
        """Detect faces using DNN"""
        if self.face_net is None:
            return self.detect_faces_haar(frame)
            
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123])
        self.face_net.setInput(blob)
        detections = self.face_net.forward()
        
        faces = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > self.confidence_threshold:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x, y, x1, y1) = box.astype("int")
                faces.append((x, y, x1-x, y1-y))
        
        return faces
    
    def detect_faces_haar(self, frame):
        """Detect faces using Haar Cascade"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )
        return faces
    
    def create_mask_detection_model(self):
        """Create a CNN model for mask detection"""
        # Use MobileNetV2 as base model for better performance
        base_model = MobileNetV2(weights="imagenet", include_top=False, 
                                input_tensor=None, input_shape=(224, 224, 3))
        
        # Create the head model
        head_model = base_model.output
        head_model = AveragePooling2D(pool_size=(7, 7))(head_model)
        head_model = Flatten(name="flatten")(head_model)
        head_model = Dense(128, activation="relu")(head_model)
        head_model = Dropout(0.5)(head_model)
        head_model = Dense(2, activation="softmax")(head_model)
        
        # Place the head FC model on top of the base model
        model = Sequential([base_model, head_model])
        
        # Freeze the base model layers
        for layer in base_model.layers:
            layer.trainable = False
            
        return model
    
    def create_simple_cnn_model(self):
        """Create a simple CNN model for mask detection"""
        model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
            MaxPooling2D(2, 2),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),
            Flatten(),
            Dropout(0.5),
            Dense(512, activation='relu'),
            Dense(2, activation='softmax')  # 2 classes: mask, no_mask
        ])
        
        return model
    
    def prepare_dataset(self, dataset_path):
        """Prepare dataset for training"""
        data = []
        labels = []
        
        # Categories
        categories = ['with_mask', 'without_mask']
        
        for category in categories:
            path = os.path.join(dataset_path, category)
            if not os.path.exists(path):
                print(f"⚠️  Directory {path} not found. Creating sample data structure...")
                continue
                
            for img_name in os.listdir(path):
                img_path = os.path.join(path, img_name)
                try:
                    image = load_img(img_path, target_size=(128, 128))
                    image = img_to_array(image)
                    image = image / 255.0
                    
                    data.append(image)
                    labels.append(category)
                except Exception as e:
                    print(f"Error loading {img_path}: {e}")
        
        # Convert to numpy arrays
        data = np.array(data, dtype="float32")
        labels = np.array(labels)
        
        # Convert labels to binary
        lb = LabelBinarizer()
        labels = lb.fit_transform(labels)
        labels = to_categorical(labels)
        
        return data, labels, lb
    
    def train_mask_detector(self, dataset_path, model_save_path="mask_detector.model"):
        """Train the mask detection model"""
        print("🚀 Loading dataset...")
        
        # Check if dataset exists
        if not os.path.exists(dataset_path):
            print(f"❌ Dataset path {dataset_path} not found!")
            print("📝 Creating sample training structure...")
            self.create_sample_dataset_structure(dataset_path)
            return None
        
        data, labels, lb = self.prepare_dataset(dataset_path)
        
        if len(data) == 0:
            print("❌ No training data found!")
            return None
        
        # Split the data
        (trainX, testX, trainY, testY) = train_test_split(data, labels,
                                                         test_size=0.20, stratify=labels, random_state=42)
        
        # Data augmentation
        aug = ImageDataGenerator(
            rotation_range=20,
            zoom_range=0.15,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.15,
            horizontal_flip=True,
            fill_mode="nearest")
        
        # Create and compile model
        model = self.create_simple_cnn_model()
        
        opt = Adam(lr=1e-4, decay=1e-4 / 20)
        model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])
        
        print("🔥 Training mask detector...")
        H = model.fit(
            aug.flow(trainX, trainY, batch_size=32),
            steps_per_epoch=len(trainX) // 32,
            validation_data=(testX, testY),
            validation_steps=len(testX) // 32,
            epochs=20)
        
        # Evaluate the model
        print("📊 Evaluating model...")
        predIdxs = model.predict(testX, batch_size=32)
        predIdxs = np.argmax(predIdxs, axis=1)
        
        print(classification_report(testY.argmax(axis=1), predIdxs,
                                  target_names=lb.classes_))
        
        # Save the model
        print(f"💾 Saving mask detector model to {model_save_path}")
        model.save(model_save_path)
        
        # Save the label binarizer
        with open("lb.pickle", "wb") as f:
            f.write(pickle.dumps(lb))
        
        self.mask_detector = model
        return model
    
    def load_mask_detector(self, model_path="mask_detector.model"):
        """Load pre-trained mask detector"""
        try:
            from tensorflow.keras.models import load_model
            self.mask_detector = load_model(model_path)
            print("✅ Mask detector model loaded successfully")
            
            # Load label binarizer
            with open("lb.pickle", "rb") as f:
                self.lb = pickle.loads(f.read())
            return True
        except Exception as e:
            print(f"❌ Error loading mask detector: {e}")
            return False
    
    def create_sample_dataset_structure(self, base_path):
        """Create sample dataset directory structure"""
        os.makedirs(os.path.join(base_path, "with_mask"), exist_ok=True)
        os.makedirs(os.path.join(base_path, "without_mask"), exist_ok=True)
        
        print(f"""
📁 Created dataset structure at {base_path}:
├── with_mask/     (Put images of people wearing masks here)
└── without_mask/  (Put images of people without masks here)

💡 To train the model:
1. Add images to the respective folders
2. Run: detector.train_mask_detector('{base_path}')
        """)
    
    def predict_mask(self, face_image):
        """Predict if a face is wearing a mask"""
        if self.mask_detector is None:
            return "Model not loaded", 0.0
        
        # Preprocess the face image
        face_image = cv2.resize(face_image, (128, 128))
        face_image = face_image.astype("float") / 255.0
        face_image = img_to_array(face_image)
        face_image = np.expand_dims(face_image, axis=0)
        
        # Make prediction
        (mask, withoutMask) = self.mask_detector.predict(face_image)[0]
        
        # Determine class label and color
        if mask > withoutMask:
            label = "Mask"
            color = (0, 255, 0)  # Green
            confidence = mask
        else:
            label = "No Mask"
            color = (0, 0, 255)  # Red
            confidence = withoutMask
            
        return label, confidence, color
    
    def detect_and_predict_mask(self, frame):
        """Detect faces and predict mask wearing"""
        # Detect faces
        faces = self.detect_faces_dnn(frame) if self.face_net else self.detect_faces_haar(frame)
        
        results = []
        for (x, y, w, h) in faces:
            # Extract face ROI
            face = frame[y:y+h, x:x+w]
            
            if face.size == 0:
                continue
                
            if self.mask_detector is not None:
                # Predict mask
                label, confidence, color = self.predict_mask(face)
            else:
                label, confidence, color = "Model not loaded", 0.0, (255, 255, 255)
            
            results.append({
                'bbox': (x, y, w, h),
                'label': label,
                'confidence': confidence,
                'color': color
            })
        
        return results
    
    def run_webcam_detection(self):
        """Run real-time face and mask detection from webcam"""
        print("🎥 Starting webcam detection...")
        print("Press 'q' to quit, 's' to save screenshot")
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Error: Could not open webcam")
            return
        
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Detect and predict every 3 frames for better performance
            if frame_count % 3 == 0:
                results = self.detect_and_predict_mask(frame)
            
            # Draw results
            for result in results:
                (x, y, w, h) = result['bbox']
                label = result['label']
                confidence = result['confidence']
                color = result['color']
                
                # Draw bounding box
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                
                # Draw label
                text = f"{label}: {confidence:.2f}"
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Add instructions
            cv2.putText(frame, "Press 'q' to quit, 's' to save", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('Face Mask Detection', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                cv2.imwrite(f'screenshot_{frame_count}.jpg', frame)
                print(f"📸 Screenshot saved: screenshot_{frame_count}.jpg")
        
        cap.release()
        cv2.destroyAllWindows()
        print("✅ Webcam detection stopped")
    
    def detect_from_image(self, image_path, save_result=True):
        """Detect faces and masks from a single image"""
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            return
        
        # Load image
        frame = cv2.imread(image_path)
        if frame is None:
            print(f"❌ Could not load image: {image_path}")
            return
        
        print(f"🖼️  Processing image: {image_path}")
        
        # Detect and predict
        results = self.detect_and_predict_mask(frame)
        
        # Draw results
        for result in results:
            (x, y, w, h) = result['bbox']
            label = result['label']
            confidence = result['confidence']
            color = result['color']
            
            # Draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            
            # Draw label
            text = f"{label}: {confidence:.2f}"
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Display results
        print(f"📊 Found {len(results)} face(s)")
        for i, result in enumerate(results):
            print(f"  Face {i+1}: {result['label']} (confidence: {result['confidence']:.2f})")
        
        # Show image
        cv2.imshow('Face Mask Detection - Press any key to close', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        # Save result
        if save_result:
            output_path = f"result_{os.path.basename(image_path)}"
            cv2.imwrite(output_path, frame)
            print(f"💾 Result saved: {output_path}")

def main():
    """Main function to demonstrate the Face Mask Detection System"""
    print("🎭 Face Recognition/Mask Detection System")
    print("=" * 50)
    
    # Initialize detector
    detector = FaceMaskDetector()
    
    # Load face detector
    detector.load_face_detector_dnn()
    
    # Try to load pre-trained mask detector
    model_loaded = detector.load_mask_detector()
    
    if not model_loaded:
        print("⚠️  No pre-trained mask detector found.")
        print("🔧 You can either:")
        print("   1. Train a new model with your dataset")
        print("   2. Use face detection only")
        
        choice = input("\nEnter 't' to train, 'c' to continue with face detection only: ")
        
        if choice.lower() == 't':
            dataset_path = input("Enter dataset path (or press Enter for default): ").strip()
            if not dataset_path:
                dataset_path = "mask_dataset"
            
            detector.train_mask_detector(dataset_path)
    
    while True:
        print("\n🎯 Choose an option:")
        print("1. 🎥 Real-time webcam detection")
        print("2. 🖼️  Detect from image file")
        print("3. 🔧 Train new model")
        print("4. 📊 Create dataset structure")
        print("5. ❌ Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            detector.run_webcam_detection()
        
        elif choice == '2':
            image_path = input("Enter image path: ")
            detector.detect_from_image(image_path)
        
        elif choice == '3':
            dataset_path = input("Enter dataset path: ")
            detector.train_mask_detector(dataset_path)
        
        elif choice == '4':
            dataset_path = input("Enter path to create dataset structure: ")
            detector.create_sample_dataset_structure(dataset_path)
        
        elif choice == '5':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()