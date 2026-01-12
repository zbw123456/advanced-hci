"""
Main Application Entry Point for MindCare System.
Integrates GUI, Camera, and Core Logic using PyQt5 and MVC pattern.
"""
import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QTimer

from gui.main_window import MainWindow
from core.fsm import FiniteStateMachine, AppState
from core.security import SecurityManager
from demo_mode import DemoEmotionGenerator, TimeWindowProcessor
from face_detector import FaceDetector

# Emotion Colors (BGR) matches demo_mode
COLORS = {
    'happy': (68, 255, 68),
    'neutral': (170, 170, 170),
    'sad': (255, 68, 68),
    'angry': (68, 68, 255)
}

class CameraThread(QThread):
    new_frame = pyqtSignal(np.ndarray)
    # Signal to update dashboard with new emotion data (processed in background)
    emotion_update = pyqtSignal(dict) 

    def __init__(self, camera_index=None, emotion_generator=None):
        super().__init__()
        self.camera_index = camera_index
        self.is_running = True
        self.cap = None
        self.detector = FaceDetector()
        self.emotion_generator = emotion_generator # Passed from main app
        
    def run(self):
        # Auto-detect FaceTime camera (720p priority)
        if self.camera_index is None:
            print("Auto-detecting camera...")
            best_idx = 0
            # Scan first 5 indices
            for i in range(5):
                temp_cap = cv2.VideoCapture(i)
                if temp_cap.isOpened():
                    w = int(temp_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    h = int(temp_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    temp_cap.release()
                    print(f"Scanned Camera {i}: {w}x{h}")
                    if w == 1280 and h == 720: # FaceTime Resolution
                        best_idx = i
                        print(f"-> Selected Camera {i} (FaceTime Match)")
                        break
            
            self.cap = cv2.VideoCapture(best_idx)
        else:
            self.cap = cv2.VideoCapture(self.camera_index)
        
        # Fallback loop
        if not self.cap.isOpened():
             print("Camera init failed, trying fallback indices...")
             for i in range(3):
                 self.cap = cv2.VideoCapture(i)
                 if self.cap.isOpened(): break
        
        frame_counter = 0
        is_smiling = False # Track smile state across frames if needed, or per frame
        
        while self.is_running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame_counter += 1
                is_smiling = False # Reset per frame
                
                # Face Detection & Visualization
                try:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    face = self.detector.detect_face(gray)
                    
                    if face:
                        x, y, w, h = face
                        
                        # Check for smile
                        face_roi_gray = gray[y:y+h, x:x+w]
                        if self.detector.detect_smile(face_roi_gray):
                            is_smiling = True
                        
                        color = (68, 255, 68) # Green
                        if is_smiling:
                            color = (0, 255, 255) # Yellow for smile
                            cv2.putText(frame, "Smiling! :)", (x, y-40), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                        
                        elif self.emotion_generator:
                           curr_emo = self.emotion_generator.current_emotion
                           color = COLORS.get(curr_emo, (200, 200, 200))
                           
                        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                        cv2.putText(frame, "Face Detected", (x, y-10), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                    else:
                         cv2.putText(frame, "Searching for face...", (20, 40), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 255), 2)
                        

                            
                except Exception as e:
                    # Log error but don't clutter screen for demo
                    print(f"Detection Error: {e}")

                # DEMO MODE: Always generate emotion data to keep UI alive
                # NOW REACTIVE: Pass is_smiling to generator
                if self.emotion_generator and frame_counter % 5 == 0:
                    probs = self.emotion_generator.get_emotion_probabilities(is_smiling=is_smiling)
                    self.emotion_update.emit(probs)

                self.new_frame.emit(frame)
            else:
                self.msleep(100) # Wait a bit if frame read fails
        
        if self.cap:
            self.cap.release()

    def stop(self):
        self.is_running = False
        self.wait()

class MindCareApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        
        # Core Components
        self.fsm = FiniteStateMachine()
        self.security = SecurityManager()
        
        # Logic Components (Reused from demo for now)
        self.emotion_generator = DemoEmotionGenerator()
        self.time_processor = TimeWindowProcessor(window_size=60)
        
        # Treads
        self.camera_thread = CameraThread(emotion_generator=self.emotion_generator)
        
        # Connect Signals
        self.camera_thread.new_frame.connect(self.window.video_widget.update_frame)
        self.camera_thread.emotion_update.connect(self.process_emotion_update) # New signal connection
        
        # Connect UI Controls
        self.window.btn_start.clicked.connect(self.start_monitoring)
        self.window.btn_pause.clicked.connect(self.toggle_pause)
        self.window.btn_stop.clicked.connect(self.stop_session)
        
        # Initial State
        self.window.show()

    def start_monitoring(self):
        self.fsm.start_monitoring()
        self.window.status_bar.showMessage(f"State: {self.fsm.current_state.name} - Monitoring Started")
        if not self.camera_thread.isRunning():
            self.camera_thread.start()
        self.window.btn_start.setEnabled(False)
        self.window.btn_pause.setEnabled(True)

    def toggle_pause(self):
        if self.fsm.current_state == AppState.MONITORING:
            self.fsm.pause()
            self.window.btn_pause.setText("Resume")
            self.window.status_bar.showMessage("State: PAUSED")
        elif self.fsm.current_state == AppState.PAUSED:
            self.fsm.resume()
            self.window.btn_pause.setText("Pause")
            self.window.status_bar.showMessage("State: MONITORING")

    def stop_session(self):
        self.fsm.stop()
        self.camera_thread.stop()
        self.window.status_bar.showMessage("Session Stopped. Data Encrypted & Saved.")
        QMessageBox.information(self.window, "Session Ends", "Session data has been securely saved.")
        self.window.btn_start.setEnabled(True)
        self.window.btn_pause.setEnabled(False)
        self.window.btn_pause.setText("Pause")

    def process_emotion_update(self, probs):
        """Handle new emotion data from thread."""
        if self.fsm.current_state != AppState.MONITORING:
            return

        self.time_processor.add_prediction(probs)
        
        # Update UI
        self.window.dashboard.update_emotions(probs)
        self.window.dashboard.update_buffer(self.time_processor.get_fill_percentage())
        
        # Update stress meter
        aggregated = self.time_processor.get_aggregated_emotion()
        if aggregated:
            # Simple stress calc reuse
            valence = sum(aggregated[e] * {'happy': 0.8, 'surprised': 0.3, 'neutral': 0.0, 
                                            'sad': -0.6, 'angry': -0.7, 'fearful': -0.5, 
                                            'disgusted': -0.6}.get(e, 0) for e in aggregated)
            stress = (1.0 - (valence + 1.0) / 2.0)
            self.window.dashboard.update_stress(stress)
            
            # Check for Alert Condition
            if stress > 0.8:
                self.fsm.trigger_alert()
                self.window.status_bar.showMessage("⚠️ HIGH STRESS DETECTED")

    def run(self):
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    # Check for camera index arg if needed, else auto
    app = MindCareApp()
    app.run()
