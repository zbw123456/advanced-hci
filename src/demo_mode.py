"""
Demo mode for MindCare with enhanced visual feedback.
This version uses simulated emotion detection for demonstration purposes.
"""

import cv2
import numpy as np
import time
import random
from datetime import datetime
from collections import deque
from typing import Dict, List, Tuple
from audio_module import AudioAnalyzer

# Emotion labels
EMOTIONS = ['angry', 'disgusted', 'fearful', 'happy', 'sad', 'surprised', 'neutral']

# Color scheme (BGR format for OpenCV)
COLORS = {
    'angry': (68, 68, 255),      # Red
    'disgusted': (255, 68, 170),  # Purple
    'fearful': (68, 153, 255),    # Orange
    'happy': (68, 255, 68),       # Green
    'sad': (255, 68, 68),         # Blue
    'surprised': (68, 255, 255),  # Yellow
    'neutral': (170, 170, 170)    # Gray
}

# Valence mapping
VALENCE = {
    'happy': 0.8, 'surprised': 0.3, 'neutral': 0.0,
    'sad': -0.6, 'angry': -0.7, 'fearful': -0.5, 'disgusted': -0.6
}


class DemoEmotionGenerator:
    """Generates realistic emotion sequences for demo purposes."""
    
    def __init__(self):
        self.current_emotion = 'neutral'
        self.emotion_duration = 0
        self.transition_prob = 0.05  # 5% chance to change emotion each frame
        
    def get_emotion_probabilities(self, is_smiling: bool = False) -> Dict[str, float]:
        """Generate realistic emotion probabilities."""
        
        # REACTIVE MODE: If smile detected, force happy
        if is_smiling:
            self.current_emotion = 'happy'
            self.emotion_duration = 0
            probs = {e: 0.02 for e in EMOTIONS}
            probs['happy'] = 0.88
            return probs

        # Occasionally transition to new emotion
        if random.random() < self.transition_prob or self.emotion_duration > 90:
            # Weighted random selection (more likely to be neutral/happy)
            weights = [0.05, 0.02, 0.03, 0.3, 0.1, 0.05, 0.45]
            self.current_emotion = random.choices(EMOTIONS, weights=weights)[0]
            self.emotion_duration = 0
        
        self.emotion_duration += 1
        
        # Create probability distribution centered on current emotion
        probs = {}
        for emotion in EMOTIONS:
            if emotion == self.current_emotion:
                probs[emotion] = random.uniform(0.6, 0.9)
            else:
                probs[emotion] = random.uniform(0.01, 0.1)
        
        # Normalize
        total = sum(probs.values())
        probs = {k: v/total for k, v in probs.items()}
        
        return probs


class TimeWindowProcessor:
    """Processes emotions over time windows."""
    
    def __init__(self, window_size: int = 60):
        self.window_size = window_size
        self.buffer = deque(maxlen=window_size)
        
    def add_prediction(self, emotion_probs: Dict[str, float]):
        """Add emotion prediction to buffer."""
        self.buffer.append(emotion_probs)
        
    def get_aggregated_emotion(self) -> Dict[str, float]:
        """Get aggregated emotion over window."""
        if not self.buffer:
            return {e: 1.0/len(EMOTIONS) for e in EMOTIONS}
        
        aggregated = {emotion: 0.0 for emotion in EMOTIONS}
        for probs in self.buffer:
            for emotion, prob in probs.items():
                aggregated[emotion] += prob
        
        # Normalize
        num_frames = len(self.buffer)
        aggregated = {k: v/num_frames for k, v in aggregated.items()}
        
        return aggregated
    
    def get_fill_percentage(self) -> float:
        """Get buffer fill percentage."""
        return len(self.buffer) / self.window_size


class VoiceCommandSimulator:
    """Simulates voice commands via keyboard."""
    
    def __init__(self):
        self.active_command = None
        self.command_start_time = None
        self.command_duration = 2.0  # seconds
        
        self.commands = {
            ord('1'): {
                'text': '🎤 "Hey MindCare, how am I doing?"',
                'response': 'Your current mood is {emotion}\nwith {confidence:.0%} confidence.'
            },
            ord('2'): {
                'text': '🎤 "Pause monitoring"',
                'response': 'Monitoring paused.\nPress 3 to resume.'
            },
            ord('3'): {
                'text': '🎤 "Resume monitoring"',
                'response': 'Monitoring resumed.'
            },
            ord('4'): {
                'text': '🎤 "Show statistics"',
                'response': 'Session duration: {duration}\nEmotions detected: {count}'
            }
        }
    
    def trigger_command(self, key: int, context: Dict = None):
        """Trigger a voice command."""
        if key in self.commands:
            self.active_command = self.commands[key].copy()
            self.command_start_time = time.time()
            
            # Format response with context
            if context:
                self.active_command['response'] = self.active_command['response'].format(**context)
    
    def get_active_command(self) -> Tuple[str, str, float]:
        """Get active command if any."""
        if self.active_command is None:
            return None
        
        elapsed = time.time() - self.command_start_time
        if elapsed > self.command_duration:
            self.active_command = None
            return None
        
        progress = elapsed / self.command_duration
        return (self.active_command['text'], 
                self.active_command['response'], 
                progress)


class MindCareDemoApp:
    """Enhanced demo mode for MindCare."""
    
    def __init__(self, camera_index=None):
        self.camera_index = camera_index
        self.emotion_generator = DemoEmotionGenerator()
        self.time_processor = TimeWindowProcessor(window_size=60)
        self.voice_simulator = VoiceCommandSimulator()
        self.audio_analyzer = AudioAnalyzer()
        
        self.cap = None
        self.face_cascade = None
        self.is_running = False
        self.is_paused = False
        
        self.emotion_history = []
        self.start_time = time.time()
        self.frame_count = 0
        self.fps = 0
        self.last_fps_time = time.time()
        
        # Load face detector
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
    def initialize_camera(self, camera_index=None) -> bool:
        """Initialize camera, trying multiple indices if needed."""
        # Use instance preference if no arg provided
        if camera_index is None:
            camera_index = self.camera_index

        # Try different camera indices
        camera_indices = [camera_index] if camera_index is not None else [0, 1, 2]
        
        for idx in camera_indices:
            print(f"Trying camera index {idx}...")
            # Try AP_AVFOUNDATION for Mac
            self.cap = cv2.VideoCapture(idx, cv2.CAP_AVFOUNDATION)
            if not self.cap.isOpened():
                 self.cap = cv2.VideoCapture(idx)
            
            if self.cap.isOpened():
                # Warm up camera
                print(f"  Camera {idx} opened. Warming up...")
                for i in range(10): # Try for 1 second
                    ret, test_frame = self.cap.read()
                    if ret and test_frame is not None:
                        print(f"  Frame captured! Resolution: {test_frame.shape}")
                        # Found a working frame
                        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                        self.cap.set(cv2.CAP_PROP_FPS, 30)
                        
                        print(f"✓ Camera initialized (index {idx})")
                        return True
                    time.sleep(0.1)
                
                # If we get here, we failed to read frames after opening
                self.cap.release()
                print(f"  Camera {idx} opened but cannot read frames (timeout)")
            else:
                print(f"  Camera {idx} not available")
        
        print("❌ No working camera found")
        return False
    
    def detect_face(self, frame: np.ndarray) -> Tuple[int, int, int, int]:
        """Detect face in frame."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(48, 48)
        )
        
        if len(faces) == 0:
            return None
        
        # Return largest face
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        return tuple(largest_face)
    
    def draw_emotion_bars(self, frame: np.ndarray, emotion_probs: Dict[str, float], 
                         x: int, y: int, width: int = 200):
        """Draw emotion probability bars."""
        bar_height = 25
        spacing = 5
        
        # Sort by probability
        sorted_emotions = sorted(emotion_probs.items(), key=lambda x: x[1], reverse=True)
        
        for i, (emotion, prob) in enumerate(sorted_emotions):
            y_pos = y + i * (bar_height + spacing)
            
            # Background
            cv2.rectangle(frame, (x, y_pos), (x + width, y_pos + bar_height), 
                         (40, 40, 40), -1)
            
            # Probability bar
            bar_width = int(width * prob)
            color = COLORS[emotion]
            cv2.rectangle(frame, (x, y_pos), (x + bar_width, y_pos + bar_height), 
                         color, -1)
            
            # Text
            text = f"{emotion.capitalize()} {prob:.2f}"
            cv2.putText(frame, text, (x + 5, y_pos + 18), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def draw_time_window_buffer(self, frame: np.ndarray, fill_pct: float, 
                                x: int, y: int, width: int = 200):
        """Draw time window buffer visualization."""
        height = 30
        
        # Background
        cv2.rectangle(frame, (x, y), (x + width, y + height), (40, 40, 40), -1)
        
        # Fill
        fill_width = int(width * fill_pct)
        cv2.rectangle(frame, (x, y), (x + fill_width, y + height), (68, 255, 68), -1)
        
        # Text
        text = f"Buffer: {fill_pct:.0%}"
        cv2.putText(frame, text, (x + 5, y + 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def draw_stress_meter(self, frame: np.ndarray, valence: float, 
                         x: int, y: int, width: int = 200):
        """Draw stress level meter."""
        height = 30
        
        # Calculate stress level (inverse of valence)
        stress = (1.0 - (valence + 1.0) / 2.0)  # Convert -1..1 to 0..1
        
        # Background
        cv2.rectangle(frame, (x, y), (x + width, y + height), (40, 40, 40), -1)
        
        # Stress bar (green to red gradient)
        fill_width = int(width * stress)
        if stress < 0.3:
            color = (68, 255, 68)  # Green
        elif stress < 0.6:
            color = (68, 255, 255)  # Yellow
        else:
            color = (68, 68, 255)  # Red
        
        cv2.rectangle(frame, (x, y), (x + fill_width, y + height), color, -1)
        
        # Text
        text = f"Stress: {stress:.0%}"
        cv2.putText(frame, text, (x + 5, y + 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def draw_voice_command_overlay(self, frame: np.ndarray, command_text: str, 
                                   response: str, progress: float):
        """Draw voice command overlay."""
        h, w = frame.shape[:2]
        
        # Semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (50, h//2 - 100), (w - 50, h//2 + 100), 
                     (30, 30, 30), -1)
        cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
        
        # Command text
        cv2.putText(frame, command_text, (70, h//2 - 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (68, 255, 255), 2)
        
        # Processing animation
        if progress < 0.3:
            status = "Processing... ⏳"
        elif progress < 0.6:
            status = "Analyzing... 🔍"
        else:
            status = "Response:"
        
        cv2.putText(frame, status, (70, h//2 - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        # Response (show after processing)
        if progress > 0.5:
            y_offset = h//2 + 20
            for line in response.split('\n'):
                cv2.putText(frame, line, (70, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                y_offset += 30
    
    def draw_help_overlay(self, frame: np.ndarray):
        """Draw help overlay."""
        h, w = frame.shape[:2]
        
        # Semi-transparent background
        overlay = frame.copy()
        cv2.rectangle(overlay, (w - 280, 10), (w - 10, 250), (30, 30, 30), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Help text
        help_text = [
            "CONTROLS:",
            "q - Quit",
            "p - Pause/Resume",
            "h - Toggle help",
            "",
            "VOICE COMMANDS:",
            "1 - How am I doing?",
            "2 - Pause",
            "3 - Resume",
            "4 - Statistics"
        ]
        
        y_offset = 35
        for line in help_text:
            cv2.putText(frame, line, (w - 270, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
            y_offset += 22

    def draw_audio_panel(self, frame: np.ndarray, x: int, y: int, width: int, height: int):
        """Draw audio waveform and emotion analysis."""
        # Background
        cv2.rectangle(frame, (x, y), (x + width, y + height), (20, 20, 20), -1)
        
        # Audio Title
        cv2.putText(frame, "AUDIO ANALYSIS", (x + 10, y + 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Get data
        audio_state = self.audio_analyzer.get_current_state()
        waveform = self.audio_analyzer.get_waveform()
        
        # Draw waveform
        if waveform:
            center_y = y + height // 2 + 10
            points = []
            for i, val in enumerate(waveform):
                px = int(x + 10 + (i / len(waveform)) * (width - 20))
                py = int(center_y + val * (height / 3))
                points.append((px, py))
            
            if len(points) > 1:
                cv2.polylines(frame, [np.array(points)], False, (0, 255, 255), 1)
        
        # Draw Emotion Tag
        emotion = audio_state["emotion"]
        color = (100, 100, 100)
        if emotion != "silence":
            color = COLORS.get(emotion, (255, 255, 255))
        
        cv2.putText(frame, f"Detected: {emotion.upper()}", (x + width - 180, y + 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        # Draw Energy Bar
        energy = audio_state["energy"]
        bar_w = 100
        bar_h = 6
        bar_x = x + width - 120
        bar_y = y + 40
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), (50, 50, 50), -1)
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + int(bar_w * energy), bar_y + bar_h), (0, 255, 0), -1)
        cv2.putText(frame, "Energy", (bar_x - 50, bar_y + 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 150, 150), 1)
    
    def run(self):
        """Run the demo."""
        if not self.initialize_camera():
            print("Using demo mode without camera")
            return
        
        self.is_running = True
        show_help = True
        
        print("\n" + "="*60)
        print("MINDCARE DEMO MODE")
        print("="*60)
        print("Press 'h' to toggle help")
        print("Press 'q' to quit")
        print()
        
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to read frame")
                break
            
            self.frame_count += 1
            
            # Calculate FPS
            current_time = time.time()
            if current_time - self.last_fps_time >= 1.0:
                self.fps = self.frame_count / (current_time - self.last_fps_time)
                self.frame_count = 0
                self.last_fps_time = current_time
            
            # Create display frame (larger for UI elements)
            h, w = frame.shape[:2]
            display = np.zeros((h + 250, w, 3), dtype=np.uint8)
            display[:h, :w] = frame
            
            if not self.is_paused:
                # Detect face
                bbox = self.detect_face(frame)
                
                if bbox is not None:
                    x, y, w_face, h_face = bbox
                    
                    # Generate emotion probabilities
                    emotion_probs = self.emotion_generator.get_emotion_probabilities()
                    self.time_processor.add_prediction(emotion_probs)
                    
                    # Get aggregated emotion
                    if self.frame_count % 30 == 0:  # Every ~1 second
                        aggregated = self.time_processor.get_aggregated_emotion()
                        dominant_emotion = max(aggregated.items(), key=lambda x: x[1])
                        
                        # Calculate valence
                        valence = sum(aggregated[e] * VALENCE[e] for e in EMOTIONS)
                        
                        # Record to history
                        self.emotion_history.append({
                            'emotion': dominant_emotion[0],
                            'confidence': dominant_emotion[1],
                            'valence': valence,
                            'timestamp': datetime.now()
                        })
                    
                    # Draw face box
                    color = COLORS[self.emotion_generator.current_emotion]
                    cv2.rectangle(display, (x, y), (x + w_face, y + h_face), color, 2)
                    
                    # Label
                    label = f"{self.emotion_generator.current_emotion.upper()}"
                    cv2.putText(display, label, (x, y - 10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                    
                    # Draw emotion bars
                    self.draw_emotion_bars(display, emotion_probs, 10, h + 10)
                    
                    # Draw time window buffer
                    fill_pct = self.time_processor.get_fill_percentage()
                    self.draw_time_window_buffer(display, fill_pct, 220, h + 10)
                    
                    # Draw stress meter
                    if self.emotion_history:
                        valence = self.emotion_history[-1]['valence']
                        self.draw_stress_meter(display, valence, 430, h + 10)
                    
                else:
                    # No face detected
                    cv2.putText(display, "No face detected", (20, 50), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
            
            # Status bar
            status_y = h + 60
            status_text = f"FPS: {self.fps:.1f} | State: {'PAUSED' if self.is_paused else 'MONITORING'} | Emotions: {len(self.emotion_history)}"
            cv2.putText(display, status_text, (10, status_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Voice command overlay
            command_info = self.voice_simulator.get_active_command()
            if command_info:
                self.draw_voice_command_overlay(display, *command_info)
            
            # Help overlay
            if show_help:
                self.draw_help_overlay(display)
            
            # Show frame
            cv2.imshow('MindCare Demo', display)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                self.is_running = False
            elif key == ord('p'):
                self.is_paused = not self.is_paused
                print(f"{'PAUSED' if self.is_paused else 'RESUMED'}")
            elif key == ord('h'):
                show_help = not show_help
            elif key in [ord('1'), ord('2'), ord('3'), ord('4')]:
                # Trigger voice command
                context = {}
                if self.emotion_history:
                    context['emotion'] = self.emotion_history[-1]['emotion'].upper()
                    context['confidence'] = self.emotion_history[-1]['confidence']
                
                duration = int(time.time() - self.start_time)
                context['duration'] = f"{duration // 60}m {duration % 60}s"
                context['count'] = len(self.emotion_history)
                
                self.voice_simulator.trigger_command(key, context)
                
                # Handle pause/resume
                if key == ord('2'):
                    self.is_paused = True
                elif key == ord('3'):
                    self.is_paused = False
        
        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()
        
        # Print summary
        print("\n" + "="*60)
        print("SESSION SUMMARY")
        print("="*60)
        print(f"Duration: {int(time.time() - self.start_time)}s")
        print(f"Emotions detected: {len(self.emotion_history)}")
        
        if self.emotion_history:
            emotion_counts = {}
            for entry in self.emotion_history:
                emotion = entry['emotion']
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            print("\nEmotion Distribution:")
            for emotion, count in sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True):
                pct = count / len(self.emotion_history) * 100
                print(f"  {emotion:10s}: {pct:5.1f}% ({count})")


def main():
    """Entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='MindCare Demo')
    parser.add_argument('--camera', type=int, default=None,
                       help='Camera index to use (default: auto-detect)')
    args = parser.parse_args()
    
    app = MindCareDemoApp(camera_index=args.camera)
    
    if args.camera is not None:
        print(f"Using camera index: {args.camera}")
    
    app.run()


if __name__ == "__main__":
    main()
