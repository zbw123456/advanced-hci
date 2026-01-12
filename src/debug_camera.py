import cv2
import time
import sys

def test_camera(index, api_preference=None, api_name="Default"):
    print(f"\n--- Testing Camera {index} with API: {api_name} ---")
    
    if api_preference is not None:
        cap = cv2.VideoCapture(index, api_preference)
    else:
        cap = cv2.VideoCapture(index)
        
    if not cap.isOpened():
        print("❌ Failed to open camera.")
        return False
    
    print("✅ Camera opened. Waiting for hardware initialization...")
    time.sleep(2.0)  # Give camera time to warm up
    
    # Try reading a few frames
    success_count = 0
    for i in range(10):
        ret, frame = cap.read()
        if ret and frame is not None and frame.size > 0:
            success_count += 1
            print(f"  Frame {i}: OK ({frame.shape})")
        else:
            print(f"  Frame {i}: Failed (ret={ret})")
        time.sleep(0.1)
        
    cap.release()
    
    if success_count > 0:
        print(f"🎉 Success! Read {success_count}/10 frames.")
        return True
    else:
        print("❌ Opened but failed to read valid frames.")
        return False

print(f"OpenCV Version: {cv2.__version__}")

# Test Camera 1 specifically
print("\nTrying to access FaceTime Camera (Index 1)...")

# 1. Try Default
if not test_camera(1, None, "Default"):
    # 2. Try AVFoundation explicitly (macOS native)
    test_camera(1, cv2.CAP_AVFOUNDATION, "CAP_AVFOUNDATION")
    
    # 3. Try V4L2 (unlikely on Mac but worth checking logic)
    # test_camera(1, cv2.CAP_V4L2, "CAP_V4L2") 
    
    # 4. Try Index 0 just in case indices shifted
    print("\nChecking Index 0 just in case...")
    test_camera(0, cv2.CAP_AVFOUNDATION, "Index 0 + AVFoundation")
