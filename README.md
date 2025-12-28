# MindCare - Mental Well-being Monitoring System

Advanced HCI Project 2025-2026

## Overview

MindCare is an intelligent mental well-being monitoring system that uses facial expression recognition combined with multimodal interaction (camera, voice, touch) to passively detect stress and anxiety levels, providing real-time feedback and personalized recommendations.

## Features

- **Real-time Facial Expression Detection**: Continuous emotion monitoring using webcam
- **Time-Window Aggregation**: Smooths predictions over 2-second windows to reduce noise
- **Stress Pattern Detection**: Analyzes emotion trends every 30 seconds
- **Privacy-First Design**: All processing happens locally, no cloud uploads
- **Multimodal Interaction**: Camera (passive monitoring) + Voice/Touch interfaces

## Requirements

### Hardware
- Webcam (minimum 720p, 30fps recommended)
- Processor: Intel i5 or equivalent, 2.5GHz+
- RAM: 8GB minimum
- OS: macOS 11+, Windows 10+, or Ubuntu 20.04+

### Software
- Python 3.8 or higher
- See `requirements.txt` for Python dependencies

## Installation

1. **Clone or download this project**
   ```bash
   cd "/Users/bzhang/Downloads/Advanced HCI"
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download a pre-trained emotion model (optional)**
   
   The system includes a demo CNN model that is NOT trained. For actual use, download a pre-trained model:
   
   - Option 1: Download from [face_classification](https://github.com/oarriaga/face_classification)
   - Option 2: Train your own on FER-2013 dataset
   
   Place the model file at: `data/models/emotion_model.h5`

## Usage

### Basic Usage

Run the application:

```bash
cd src
python main.py
```

**Controls:**
- `q` - Quit the application
- `p` - Pause/Resume monitoring

### What to Expect

1. **Initialization**: The app loads the face detector and emotion classifier
2. **Hardware Check**: Verifies camera is available
3. **Monitoring**: Real-time emotion detection with colored bounding boxes
4. **Status Updates**: Console prints emotion status every ~1 second
5. **Pattern Alerts**: Warnings if sustained stress is detected
6. **Session Summary**: Emotion distribution and statistics when you quit

### Example Output

```
MindCare v1.0.0
Initializing...
Loading face detector...
Loading emotion classifier...
✓ Initialization complete
Checking camera...
✓ Camera found and accessible

==================================================
MONITORING STARTED
==================================================
Press 'q' to quit, 'p' to pause/resume

[14:23:15] Emotion: NEUTRAL    | Confidence: 0.78 | Valence: +0.02
[14:23:16] Emotion: HAPPY      | Confidence: 0.65 | Valence: +0.52
[14:23:17] Emotion: NEUTRAL    | Confidence: 0.82 | Valence: +0.05
...

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
⚠️  STRESS PATTERN DETECTED
   Negative emotions: 65.0% over last 20 readings
   Suggestion: Consider taking a short break
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```

## Project Structure

```
Advanced HCI/
├── src/
│   ├── main.py                 # Main application controller
│   ├── config.py               # Configuration settings
│   ├── face_detector.py        # Face detection module
│   └── emotion_classifier.py   # Emotion classification module
├── data/
│   ├── models/                 # Pre-trained models
│   └── logs/                   # Emotion logs
├── tests/                      # Unit tests (future)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── part1_problem_solution.md   # Part I: Problem definition
├── literature_review.md        # Part I: Literature review
├── part2_user_design.md        # Part II: Persona & scenario
├── system_design.md            # Part II: System architecture
└── part3_behavioral_model.md   # Part III: FSM specification
```

## Implementation Details

### Time-Window Processing

The system implements sliding window aggregation:
- Window size: 2 seconds (60 frames at 30fps)
- Overlap: Continuous sliding
- Aggregation: Weighted average of emotion probabilities
- Output: Smoothed emotion classification every ~1 second

### Stress Pattern Detection

Pattern checking occurs every 30 seconds:
- Analyzes last 15 minutes of emotion data
- Calculates ratio of negative emotions (sad, angry, fearful, disgusted)
- Threshold: 60% negative emotions
- Alert: Console warning with suggestions

### Privacy Features

- **No Frame Storage**: Raw video frames are never saved to disk
- **Local Processing**: All computation happens on your device
- **User Control**: Easy pause/resume, clear data retention policies

## Limitations

1. **Demo Model**: The included CNN model is untrained - predictions are random
   - Download a real model for actual use
2. **Single Modality**: Current implementation focuses on camera input
   - Voice and touch features are documented but not fully implemented
3. **Limited Recommendations**: Basic rule-based suggestions
4. **No Database**: Emotion history is in-memory only (not persisted)

## Future Enhancements

- Full PyQt5 GUI with rich visualizations
- Voice command interface
- Persistent database with encryption
- Advanced pattern analysis (weekly trends, correlations)
- Integration with calendar for context-aware monitoring
- Breathing exercise modules
- Export functionality (CSV, JSON)

## Troubleshooting

### Camera not found
- Ensure webcam is connected
- Check camera permissions in system settings
- Try a different camera index in `config.py` (set `CAMERA_INDEX`)

### Low Accuracy
- Ensure good lighting conditions
- Position face clearly in frame
- Download a properly trained model

### Performance Issues
- Reduce camera resolution in `config.py`
- Close other camera-using applications

## References

See `literature_review.md` for detailed scientific references on facial expression recognition and multimodal affective computing for mental health.

## Author

Advanced HCI Project 2025-2026  
University of Trento

## License

Educational project - not for commercial use.

---

**Note**: This is a prototype system for educational purposes. It should NOT be used as a replacement for professional mental health services. If you're experiencing mental health issues, please consult with a qualified healthcare provider.
