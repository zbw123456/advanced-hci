#!/usr/bin/env python3
import cv2
import os
import sys

def find_facetime_camera():
    print("🔍 Scanning for FaceTime Camera (looking for 1280x720)...")
    
    candidates = []
    
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            cap.release()
            
            print(f"  Index {i}: {w}x{h} @ {fps:.0f}FPS")
            
            # Prioritize 720p (standard FaceTime HD)
            if w == 1280 and h == 720:
                print(f"  ✨ Found match at Index {i}!")
                return i
            
            candidates.append(i)
    
    # If no exact match, try the last one (often built-in is last if others are virtual)
    # OR first one if only one exists
    if candidates:
        print(f"  ⚠️ No exact 720p match. Trying Index {candidates[-1]}...")
        return candidates[-1]
        
    return None

if __name__ == "__main__":
    idx = find_facetime_camera()
    if idx is not None:
        print(f"\n🚀 Starting Demo with Camera {idx}...")
        # Activate virtual env and run
        cmd = f"python demo_mode.py --camera {idx}"
        os.system(cmd)
    else:
        print("❌ No cameras found.")
