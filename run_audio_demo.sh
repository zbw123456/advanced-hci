#!/bin/bash
# Run MindCare Audio Demo (Standalone)

echo "🎤 MindCare Audio Emotion Recognition Demo"
echo "=========================================="
echo "Focus: Real-time audio waveform and emotion classification"
echo ""

# Activate virtual environment
source venv/bin/activate

# Run audio demo
cd src
python audio_demo.py
