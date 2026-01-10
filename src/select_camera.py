#!/usr/bin/env python3
"""
Camera selector - helps you find the right camera index for FaceTime camera
"""

import cv2
import sys

def list_cameras(max_cameras=5):
    """List all available cameras."""
    print("\n🎥 Scanning for cameras...\n")
    
    available_cameras = []
    
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                
                print(f"✅ Camera {i}:")
                print(f"   Resolution: {width}x{height}")
                print(f"   FPS: {fps}")
                print()
                
                available_cameras.append(i)
            cap.release()
    
    if not available_cameras:
        print("❌ No cameras found!")
        return None
    
    print(f"Found {len(available_cameras)} camera(s): {available_cameras}")
    print("\n💡 Tip: FaceTime camera is usually index 0 or 1")
    print("   OBS Virtual Camera might be at a different index")
    
    return available_cameras

def test_camera(camera_index):
    """Test a specific camera with face detection."""
    print(f"\n🎬 Testing camera {camera_index}...")
    print("Press 'q' to quit, 's' to select this camera\n")
    
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"❌ Cannot open camera {camera_index}")
        return False
    
    # Load face detector
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    
    selected = False
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame")
            break
        
        # Detect faces
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(48, 48))
        
        # Draw face boxes
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "Face Detected!", (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Add camera info
        cv2.putText(frame, f"Camera {camera_index}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, "Press 's' to select, 'q' to quit", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        cv2.imshow(f'Camera {camera_index} Test', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            selected = True
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    return selected

def main():
    """Main function."""
    print("="*60)
    print("MindCare Camera Selector")
    print("="*60)
    
    # List available cameras
    cameras = list_cameras()
    
    if not cameras:
        return
    
    # Ask user which camera to test
    print("\n" + "="*60)
    print("Which camera do you want to test?")
    for idx in cameras:
        print(f"  {idx} - Camera {idx}")
    print("="*60)
    
    while True:
        try:
            choice = input("\nEnter camera index (or 'a' to test all): ").strip()
            
            if choice.lower() == 'a':
                # Test all cameras
                for idx in cameras:
                    if test_camera(idx):
                        print(f"\n✅ Selected camera {idx}")
                        save_choice(idx)
                        return
            else:
                idx = int(choice)
                if idx in cameras:
                    if test_camera(idx):
                        print(f"\n✅ Selected camera {idx}")
                        save_choice(idx)
                        return
                else:
                    print(f"❌ Camera {idx} not available. Choose from: {cameras}")
        except ValueError:
            print("Invalid input. Enter a number or 'a'")
        except KeyboardInterrupt:
            print("\n\nCancelled")
            return

def save_choice(camera_index):
    """Save camera choice to config file."""
    config_file = "camera_config.txt"
    with open(config_file, 'w') as f:
        f.write(str(camera_index))
    print(f"\n💾 Saved camera index {camera_index} to {config_file}")
    print("\nNow run the demo with:")
    print(f"  python demo_mode.py --camera {camera_index}")
    print("or")
    print("  ./run_demo.sh")

if __name__ == "__main__":
    main()
