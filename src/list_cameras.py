import cv2

print("Checking camera indices...")
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        backend = cap.getBackendName()
        print(f"Index {i}: {width}x{height} @ {fps}FPS (Backend: {backend})")
        cap.release()
    else:
        print(f"Index {i}: Not available")
