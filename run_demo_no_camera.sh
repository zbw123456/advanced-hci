#!/bin/bash
# Quick start script for MindCare Demo (No Camera Version)

echo "🧠 MindCare Demo - No Camera Version"
echo "====================================="
echo ""
echo "This version uses simulated video feed"
echo "Perfect for demonstration!"
echo ""

# Activate virtual environment
source venv/bin/activate

# Run demo
cd src
python demo_no_camera.py
