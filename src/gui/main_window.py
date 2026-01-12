"""
Main Window for MindCare Application.
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFrame, QStatusBar)
from PyQt5.QtCore import Qt, pyqtSlot
from .video_widget import VideoWidget
from .dashboard import DashboardPanel
from .styles import DARK_THEME

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MindCare - AI Mental Well-being Monitor")
        self.resize(1200, 800)
        self.setStyleSheet(DARK_THEME)
        
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main Layout (Horizontal)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # --- LEFT PANEL (Video) ---
        left_panel = QFrame()
        left_panel.setObjectName("Panel")
        left_layout = QVBoxLayout(left_panel)
        
        self.video_widget = VideoWidget()
        
        left_layout.addWidget(QLabel("Live Monitor", objectName="Header"))
        left_layout.addWidget(self.video_widget, stretch=1)
        
        # --- RIGHT PANEL (Dashboard) ---
        right_panel = QFrame()
        right_panel.setObjectName("Panel")
        right_layout = QVBoxLayout(right_panel)
        
        self.dashboard = DashboardPanel()
        
        right_layout.addWidget(QLabel("Analysis Dashboard", objectName="Header"))
        right_layout.addWidget(self.dashboard)

        
        # --- ADD PANELS TO MAIN LAYOUT ---
        main_layout.addWidget(left_panel, stretch=65)
        main_layout.addWidget(right_panel, stretch=35)
        
        # --- BOTTOM CONTROLS ---
        controls_layout = QHBoxLayout()
        
        self.btn_start = QPushButton("Start Monitoring")
        self.btn_pause = QPushButton("Pause")
        self.btn_stop = QPushButton("Stop Session")
        self.btn_stop.setObjectName("StopButton")
        
        controls_layout.addWidget(self.btn_start)
        controls_layout.addWidget(self.btn_pause)
        controls_layout.addWidget(self.btn_stop)
        
        # Add controls to left panel for now, or separate bar?
        # Let's put controls at bottom of left panel
        left_layout.addLayout(controls_layout)
        
        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("System Ready")

    @pyqtSlot()
    def closeEvent(self, event):
        """Handle cleanup on close."""
        print("Closing application...")
        event.accept()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
