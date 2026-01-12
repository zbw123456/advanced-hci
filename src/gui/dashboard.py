"""
Dashboard Panel for Statistics and Metrics.
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QProgressBar, QFrame, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSlot

class DashboardPanel(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # --- Stress Meter ---
        stress_frame = QFrame()
        stress_frame.setObjectName("Panel")
        stress_layout = QVBoxLayout(stress_frame)
        
        stress_layout.addWidget(QLabel("Stress Level"))
        self.stress_bar = QProgressBar()
        self.stress_bar.setRange(0, 100)
        self.stress_bar.setValue(0)
        self.stress_bar.setTextVisible(True)
        stress_layout.addWidget(self.stress_bar)
        
        layout.addWidget(stress_frame)
        
        # --- Time Window Buffer ---
        buffer_frame = QFrame()
        buffer_frame.setObjectName("Panel")
        buffer_layout = QVBoxLayout(buffer_frame)
        
        buffer_layout.addWidget(QLabel("Time Window Buffer"))
        self.buffer_bar = QProgressBar()
        self.buffer_bar.setRange(0, 100)
        self.buffer_bar.setValue(0)
        self.buffer_bar.setStyleSheet("QProgressBar::chunk { background-color: #0d6efd; }")
        buffer_layout.addWidget(self.buffer_bar)
        
        layout.addWidget(buffer_frame)
        
        # --- Emotion Probabilities ---
        emotion_frame = QFrame()
        emotion_frame.setObjectName("Panel")
        emotion_layout = QGridLayout(emotion_frame)
        
        self.emotion_bars = {}
        emotions = ['Happy', 'Sad', 'Angry', 'Surprised', 'Fearful', 'Disgusted', 'Neutral']
        
        for i, emotion in enumerate(emotions):
            label = QLabel(emotion)
            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setValue(0)
            bar.setFixedHeight(15)
            bar.setTextVisible(False)
            
            # Custom colors
            color = self._get_color(emotion.lower())
            bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {color}; }}")
            
            # Grid: Label, Bar, Percentage Text
            emotion_layout.addWidget(label, i, 0)
            emotion_layout.addWidget(bar, i, 1)
            
            self.emotion_bars[emotion.lower()] = bar
            
        layout.addWidget(emotion_frame)
        layout.addStretch()

    def _get_color(self, emotion):
        colors = {
            'angry': '#ff4444',
            'disgusted': '#ff44aa',
            'fearful': '#ff9944',
            'happy': '#44ff44',
            'sad': '#4444ff',
            'surprised': '#44ffff',
            'neutral': '#aaaaaa'
        }
        return colors.get(emotion, '#ffffff')

    @pyqtSlot(dict)
    def update_emotions(self, probs: dict):
        """Update emotion bars from dictionary {emotion: probability}."""
        for emotion, prob in probs.items():
            if emotion in self.emotion_bars:
                val = int(prob * 100)
                self.emotion_bars[emotion].setValue(val)
    
    @pyqtSlot(float)
    def update_stress(self, value: float):
        """Update stress bar (0.0 - 1.0)."""
        val = int(value * 100)
        self.stress_bar.setValue(val)
        
        # Change color based on stress
        if val < 30:
            color = "#28a745" # Green
        elif val < 70:
            color = "#ffc107" # Yellow
        else:
            color = "#dc3545" # Red
            
        self.stress_bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {color}; }}")

    @pyqtSlot(float)
    def update_buffer(self, value: float):
        """Update buffer fill percentage (0.0 - 1.0)."""
        self.buffer_bar.setValue(int(value * 100))
