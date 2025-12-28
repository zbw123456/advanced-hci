"""
Main application controller for MindCare.
Coordinates all components and implements the state machine.
"""

import cv2
import time
from enum import Enum, auto
from datetime import datetime
from typing import Optional, Dict
import numpy as np

import config
from face_detector import FaceDetector, CameraManager
from emotion_classifier import EmotionClassifier, TimeWindowProcessor


class AppState(Enum):
    """Application states for FSM."""
    INITIALIZING = auto()
    CHECKING_HARDWARE = auto()
    IDLE = auto()
    MONITORING = auto()
    DETECTING_FACE = auto()
    ERROR_NO_CAM = auto()
    ERROR_NO_FACE = auto()


class MindCareApp:
    """Main MindCare application controller."""
    
    def __init__(self):
        """Initialize the application."""
        self.state = AppState.INITIALIZING
        
        # Components
        self.camera = None
        self.face_detector = None
        self.emotion_classifier = None
        self.time_processor = None
        
        # State tracking
        self.is_running = False
        self.is_monitoring = False
        self.last_face_time = None
        self.no_face_duration = 0
        
        # Emotion history
        self.emotion_history = []
        self.last_pattern_check = time.time()
        
        print(f"{config.APP_NAME} v{config.APP_VERSION}")
        print("Initializing...")
        
    def initialize(self) -> bool:
        """
        Initialize all components.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Initialize face detector
            print("Loading face detector...")
            self.face_detector = FaceDetector(method='haar')
            
            # Initialize emotion classifier
            print("Loading emotion classifier...")
            self.emotion_classifier = EmotionClassifier()
            
            # Initialize time window processor
            self.time_processor = TimeWindowProcessor()
            
            print("✓ Initialization complete")
            self.state = AppState.CHECKING_HARDWARE
            return True
            
        except Exception as e:
            print(f"✗ Initialization failed: {e}")
            return False
    
    def check_hardware(self) -> bool:
        """
        Check camera availability.
        
        Returns:
            True if camera is available, False otherwise
        """
        print("Checking camera...")
        self.camera = CameraManager(config.CAMERA_INDEX)
        
        if self.camera.open():
            print("✓ Camera found and accessible")
            self.state = AppState.IDLE
            return True
        else:
            print("✗ Camera not found or not accessible")
            self.state = AppState.ERROR_NO_CAM
            return False
    
    def start_monitoring(self):
        """Start emotion monitoring."""
        if self.state != AppState.IDLE:
            print("Cannot start monitoring from current state")
            return
        
        print("\n" + "="*50)
        print("MONITORING STARTED")
        print("="*50)
        print("Press 'q' to quit, 'p' to pause/resume")
        print()
        
        self.is_monitoring = True
        self.state = AppState.MONITORING
        self.time_processor.clear()
        self.last_face_time = time.time()
        
        self.monitor_loop()
    
    def monitor_loop(self):
        """Main monitoring loop."""
        frame_count = 0
        
        while self.is_monitoring:
            # Read frame from camera
            frame = self.camera.read_frame()
            
            if frame is None:
                print("Failed to read frame from camera")
                self.state = AppState.ERROR_NO_CAM
                break
            
            frame_count += 1
            current_time = time.time()
            
            # Detect face
            bbox = self.face_detector.detect_face(frame)
            
            if bbox is not None:
                # Face detected
                self.last_face_time = current_time
                self.no_face_duration = 0
                self.state = AppState.DETECTING_FACE
                
                # Extract face region
                face_img = self.face_detector.extract_face_region(
                    frame, bbox, config.MODEL_INPUT_SIZE
                )
                
                # Classify emotion
                emotion_probs = self.emotion_classifier.classify_emotion(face_img)
                
                # Add to time window
                self.time_processor.add_prediction(emotion_probs, current_time)
                
                # Get aggregated emotion (every 30 frames / ~1 second)
                if frame_count % 30 == 0:
                    aggregated = self.time_processor.get_aggregated_emotion()
                    if aggregated:
                        dominant_emotion, confidence = self.emotion_classifier.get_dominant_emotion(aggregated)
                        valence, arousal = self.emotion_classifier.calculate_valence_arousal(aggregated)
                        
                        # Log to history
                        emotion_data = {
                            'timestamp': datetime.now(),
                            'emotion': dominant_emotion,
                            'confidence': confidence,
                            'valence': valence,
                            'arousal': arousal,
                            'probabilities': aggregated
                        }
                        self.emotion_history.append(emotion_data)
                        
                        # Print status
                        self.print_emotion_status(dominant_emotion, confidence, valence)
                
                # Draw visualization
                color = self.get_emotion_color(
                    max(emotion_probs.items(), key=lambda x: x[1])[0]
                )
                label = f"{max(emotion_probs.items(), key=lambda x: x[1])[0]}"
                frame = self.face_detector.draw_face_box(frame, bbox, label, color)
                
            else:
                # No face detected
                self.no_face_duration = current_time - self.last_face_time
                
                if self.no_face_duration > config.NO_FACE_TIMEOUT_SECONDS:
                    self.state = AppState.ERROR_NO_FACE
                    # Display warning on frame
                    cv2.putText(
                        frame,
                        "Please position face in frame",
                        (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 0, 255),
                        2
                    )
            
            # Check for stress patterns (every 30 seconds)
            if current_time - self.last_pattern_check > config.PATTERN_CHECK_INTERVAL:
                self.check_stress_pattern()
                self.last_pattern_check = current_time
            
            # Display frame
            cv2.imshow('MindCare - Emotion Monitor', frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\nStopping monitoring...")
                self.is_monitoring = False
                break
            elif key == ord('p'):
                print("\n[PAUSED] Press 'p' again to resume")
                while True:
                    key = cv2.waitKey(100) & 0xFF
                    if key == ord('p'):
                        print("[RESUMED]")
                        break
                    elif key == ord('q'):
                        self.is_monitoring = False
                        break
        
        # Cleanup
        cv2.destroyAllWindows()
        self.state = AppState.IDLE
        
        # Summary
        self.print_session_summary()
    
    def print_emotion_status(self, emotion: str, confidence: float, valence: float):
        """Print current emotion status."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] "
              f"Emotion: {emotion.upper():10s} | "
              f"Confidence: {confidence:.2f} | "
              f"Valence: {valence:+.2f}")
    
    def check_stress_pattern(self):
        """Check for stress patterns in recent history."""
        if len(self.emotion_history) < 5:
            return
        
        # Get last 15 minutes of data
        cutoff_time = datetime.now().timestamp() - (config.PATTERN_HISTORY_MINUTES * 60)
        recent_emotions = [
            e for e in self.emotion_history 
            if e['timestamp'].timestamp() > cutoff_time
        ]
        
        if not recent_emotions:
            return
        
        # Calculate negative emotion ratio
        negative_count = sum(
            1 for e in recent_emotions 
            if e['emotion'] in config.NEGATIVE_EMOTIONS
        )
        negative_ratio = negative_count / len(recent_emotions)
        
        # Alert if threshold exceeded
        if negative_ratio > config.STRESS_THRESHOLD:
            print("\n" + "!"*50)
            print(f"⚠️  STRESS PATTERN DETECTED")
            print(f"   Negative emotions: {negative_ratio:.1%} over last "
                  f"{len(recent_emotions)} readings")
            print(f"   Suggestion: Consider taking a short break")
            print("!"*50 + "\n")
    
    def print_session_summary(self):
        """Print summary of the monitoring session."""
        print("\n" + "="*50)
        print("SESSION SUMMARY")
        print("="*50)
        
        if not self.emotion_history:
            print("No emotions recorded")
            return
        
        # Count emotions
        emotion_counts = {}
        for entry in self.emotion_history:
            emotion = entry['emotion']
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Display distribution
        print("\nEmotion Distribution:")
        total = len(self.emotion_history)
        for emotion in sorted(emotion_counts.keys()):
            count = emotion_counts[emotion]
            percentage = (count / total) * 100
            bar = "█" * int(percentage / 2)
            print(f"  {emotion:10s}: {bar} {percentage:5.1f}% ({count})")
        
        # Average valence
        avg_valence = sum(e['valence'] for e in self.emotion_history) / len(self.emotion_history)
        print(f"\nAverage Valence: {avg_valence:+.2f} ", end="")
        if avg_valence > 0.2:
            print("(Predominantly positive)")
        elif avg_valence < -0.2:
            print("(Predominantly negative)")
        else:
            print("(Neutral)")
        
        print(f"Total readings: {len(self.emotion_history)}")
        print("="*50 + "\n")
    
    def get_emotion_color(self, emotion: str) -> tuple:
        """Get BGR color for emotion."""
        hex_color = config.COLORS.get(emotion, '#AAAAAA')
        # Convert hex to BGR
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return (b, g, r)  # OpenCV uses BGR
    
    def stop_monitoring(self):
        """Stop monitoring."""
        self.is_monitoring = False
    
    def cleanup(self):
        """Cleanup resources."""
        if self.camera:
            self.camera.close()
        print("Cleanup complete")
    
    def run(self):
        """Main run method."""
        self.is_running = True
        
        # Initialize
        if not self.initialize():
            return
        
        # Check hardware
        if not self.check_hardware():
            print("Please ensure a camera is connected and try again")
            return
        
        # Start monitoring
        try:
            self.start_monitoring()
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
        finally:
            self.cleanup()


def main():
    """Entry point."""
    app = MindCareApp()
    app.run()


if __name__ == "__main__":
    main()
