"""
Video Widget for displaying OpenCV frames in PyQt5.
"""
from PyQt5.QtWidgets import QLabel, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot
import cv2
import numpy as np

class VideoWidget(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(640, 480)
        self.setText("Waiting for Camera...")
        self.setStyleSheet("background-color: black; border-radius: 5px;")
        
    @pyqtSlot(np.ndarray)
    def update_frame(self, frame: np.ndarray):
        """Update the displayed frame from an OpenCV image."""
        if frame is None:
            return
            
        # Convert BGR (OpenCV) to RGB (Qt)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        
        # Create QImage
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        # Scale to fit widget while maintaining aspect ratio
        scaled_pixmap = QPixmap.fromImage(qt_image).scaled(
            self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        
        self.setPixmap(scaled_pixmap)
