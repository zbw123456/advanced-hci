#!/bin/bash
# Quick start script for MindCare Demo

echo "🧠 MindCare Demo - Quick Start"
echo "================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check dependencies
echo "🔍 Checking dependencies..."
python -c "import cv2; import numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Dependencies missing!"
    echo "Installing required packages..."
    pip install opencv-python numpy
fi

# Run demo
echo ""
echo "🚀 Starting MindCare Demo..."
echo ""
echo "Controls:"
echo "  q - Quit"
echo "  p - Pause/Resume"
echo "  h - Toggle help"
echo "  1-4 - Voice commands"
echo ""
echo "Press Ctrl+C to stop"
echo ""

cd src
python demo_mode.py
