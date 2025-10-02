#!/usr/bin/env python3
"""
Simple Camera Test
=================
Test camera connection and basic face detection
"""

import cv2
import sys

def test_camera():
    """Test camera functionality"""
    
    print("📹 CAMERA CONNECTION TEST")
    print("=" * 27)
    
    # Try different camera indices
    print("🔍 Searching for available cameras...")
    
    available_cameras = []
    
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                available_cameras.append(i)
                print(f"✅ Camera {i}: WORKING")
            else:
                print(f"⚠️  Camera {i}: Opens but no frames")
            cap.release()
        else:
            print(f"❌ Camera {i}: Not available")
    
    if not available_cameras:
        print("\n❌ No working cameras found!")
        print("💡 Troubleshooting:")
        print("   - Check camera permissions")
        print("   - Close other apps using camera")
        print("   - Try external USB camera")
        return
    
    print(f"\n✅ Found {len(available_cameras)} working camera(s)")
    
    # Use first available camera
    camera_index = available_cameras[0]
    print(f"🎥 Using camera {camera_index}")
    
    # Test basic face detection
    print("\n🔍 Testing face detection...")
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    if face_cascade.empty():
        print("❌ Could not load face detection model")
        return
    
    print("✅ Face detection model loaded")
    
    # Start camera preview
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("\n🚀 Starting camera preview...")
    print("🎮 Controls:")
    print("   - Press 'q' to quit")
    print("   - Press 's' to save screenshot")
    
    frame_count = 0
    face_detected = False
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("❌ Could not read frame")
            break
        
        frame_count += 1
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Draw rectangles around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, 'Face Detected', (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            if not face_detected:
                face_detected = True
                print("👤 Face detected!")
        
        # Add frame info
        cv2.putText(frame, f'Frame: {frame_count} | Faces: {len(faces)}', 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Display frame
        cv2.imshow('Camera Test - Face Detection', frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            screenshot_name = f"camera_test_screenshot.jpg"
            cv2.imwrite(screenshot_name, frame)
            print(f"📸 Screenshot saved: {screenshot_name}")
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n📊 Test Results:")
    print(f"   - Frames processed: {frame_count}")
    print(f"   - Face detection: {'✅ Working' if face_detected else '⚠️  No faces detected'}")
    print("✅ Camera test completed")

if __name__ == "__main__":
    try:
        test_camera()
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        print("💡 Make sure OpenCV is installed: pip install opencv-python")