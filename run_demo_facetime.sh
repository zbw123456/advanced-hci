#!/bin/bash
# Run MindCare Demo with FaceTime camera (Camera 1)

echo "🧠 MindCare Demo - Using FaceTime Camera"
echo "=========================================="
echo ""

# Activate virtual environment
source venv/bin/activate

# Run demo with camera 1 (FaceTime)
cd src
python demo_mode.py --camera 1
