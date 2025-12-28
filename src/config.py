"""
Configuration management for MindCare application.
Contains all system settings and constants.
"""

import os
from pathlib import Path

# Application Info
APP_NAME = "MindCare"
APP_VERSION = "1.0.0"
AUTHOR = "Advanced HCI Project"

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = DATA_DIR / "models"
LOG_DIR = DATA_DIR / "logs"
DB_PATH = DATA_DIR / "emotions.db"

# Create directories if they don't exist
for directory in [DATA_DIR, MODEL_DIR, LOG_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Camera Settings
CAMERA_INDEX = 0  # Default camera
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# Face Detection Settings
FACE_CASCADE_PATH = "haarcascade_frontalface_default.xml"
MIN_FACE_SIZE = (48, 48)
SCALE_FACTOR = 1.1
MIN_NEIGHBORS = 5

# Emotion Model Settings
EMOTION_LABELS = ['angry', 'disgusted', 'fearful', 'happy', 'sad', 'surprised', 'neutral']
MODEL_INPUT_SIZE = (48, 48)  # FER-2013 standard
MODEL_PATH = MODEL_DIR / "emotion_model.h5"

# Time Window Settings
WINDOW_SIZE_SECONDS = 2  # Aggregate emotions over 2 seconds
FRAME_BUFFER_SIZE = CAMERA_FPS * WINDOW_SIZE_SECONDS  # Number of frames in window
PATTERN_CHECK_INTERVAL = 30  # Check for stress patterns every 30 seconds
PATTERN_HISTORY_MINUTES = 15  # Analyze last 15 minutes for patterns

# Stress Detection Thresholds
NEGATIVE_EMOTIONS = ['angry', 'disgusted', 'fearful', 'sad']
STRESS_THRESHOLD = 0.6  # 60% negative emotions
STRESS_DURATION_MINUTES = 10  # Sustained for 10 minutes
NO_FACE_TIMEOUT_SECONDS = 5  # Alert if no face for 5 seconds

# UI Settings
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"
UI_UPDATE_INTERVAL_MS = 100  # Update UI every 100ms
NOTIFICATION_DURATION_SECONDS = 30  # Auto-dismiss notifications after 30s

# Privacy Settings
STORE_FRAMES = False  # Never store raw video frames
ENCRYPT_DATABASE = True
DATA_RETENTION_DAYS = 30  # Auto-delete data older than 30 days

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Color Scheme (for UI)
COLORS = {
    'angry': '#FF4444',      # Red
    'disgusted': '#AA44FF',  # Purple
    'fearful': '#FF9944',    # Orange
    'happy': '#44FF44',      # Green
    'sad': '#4444FF',        # Blue
    'surprised': '#FFFF44',  # Yellow
    'neutral': '#AAAAAA'     # Gray
}

# Valence and Arousal mapping (for emotion analysis)
EMOTION_VALENCE = {
    'happy': 0.8,
    'surprised': 0.3,
    'neutral': 0.0,
    'sad': -0.6,
    'angry': -0.7,
    'fearful': -0.5,
    'disgusted': -0.6
}

EMOTION_AROUSAL = {
    'angry': 0.8,
    'fearful': 0.7,
    'surprised': 0.7,
    'happy': 0.5,
    'disgusted': 0.4,
    'sad': -0.4,
    'neutral': 0.0
}
