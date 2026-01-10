"""
Demo mode without camera - uses simulated video for demonstration.
This version works without camera permissions.
"""

import cv2
import numpy as np
import time
from datetime import datetime
from collections import deque
from typing import Dict, List, Tuple
import random

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
        self.transition_prob = 0.05
        
    def get_emotion_probabilities(self) -> Dict[str, float]:
        """Generate realistic emotion probabilities."""
        if random.random() < self.transition_prob or self.emotion_duration > 90:
            weights = [0.05, 0.02, 0.03, 0.3, 0.1, 0.05, 0.45]
            self.current_emotion = random.choices(EMOTIONS, weights=weights)[0]
            self.emotion_duration = 0
        
        self.emotion_duration += 1
        
        probs = {}
        for emotion in EMOTIONS:
            if emotion == self.current_emotion:
                probs[emotion] = random.uniform(0.6, 0.9)
            else:
                probs[emotion] = random.uniform(0.01, 0.1)
        
        total = sum(probs.values())
        probs = {k: v/total for k, v in probs.items()}
        
        return probs


class TimeWindowProcessor:
    """Processes emotions over time windows."""
    
    def __init__(self, window_size: int = 60):
        self.window_size = window_size
        self.buffer = deque(maxlen=window_size)
        
    def add_prediction(self, emotion_probs: Dict[str, float]):
        self.buffer.append(emotion_probs)
        
    def get_aggregated_emotion(self) -> Dict[str, float]:
        if not self.buffer:
            return {e: 1.0/len(EMOTIONS) for e in EMOTIONS}
        
        aggregated = {emotion: 0.0 for emotion in EMOTIONS}
        for probs in self.buffer:
            for emotion, prob in probs.items():
                aggregated[emotion] += prob
        
        num_frames = len(self.buffer)
        aggregated = {k: v/num_frames for k, v in aggregated.items()}
        
        return aggregated
    
    def get_fill_percentage(self) -> float:
        return len(self.buffer) / self.window_size


class VoiceCommandSimulator:
    """Simulates voice commands via keyboard."""
    
    def __init__(self):
        self.active_command = None
        self.command_start_time = None
        self.command_duration = 2.0
        
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
        if key in self.commands:
            self.active_command = self.commands[key].copy()
            self.command_start_time = time.time()
            
            if context:
                self.active_command['response'] = self.active_command['response'].format(**context)
    
    def get_active_command(self) -> Tuple[str, str, float]:
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


def create_simulated_frame(width=640, height=480, face_present=True):
    """Create a simulated video frame with a face."""
    # Create gradient background
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(height):
        intensity = int(30 + (i / height) * 50)
        frame[i, :] = [intensity, intensity, intensity]
    
    if face_present:
        # Draw simulated face (ellipse)
        center_x, center_y = width // 2, height // 2
        face_width, face_height = 150, 180
        
        # Face
        cv2.ellipse(frame, (center_x, center_y), (face_width, face_height), 
                   0, 0, 360, (220, 180, 160), -1)
        
        # Eyes
        eye_y = center_y - 30
        cv2.circle(frame, (center_x - 40, eye_y), 15, (50, 50, 50), -1)
        cv2.circle(frame, (center_x + 40, eye_y), 15, (50, 50, 50), -1)
        cv2.circle(frame, (center_x - 40, eye_y), 8, (255, 255, 255), -1)
        cv2.circle(frame, (center_x + 40, eye_y), 8, (255, 255, 255), -1)
        
        # Nose
        nose_points = np.array([
            [center_x, center_y],
            [center_x - 10, center_y + 20],
            [center_x + 10, center_y + 20]
        ])
        cv2.fillPoly(frame, [nose_points], (200, 160, 140))
        
        # Mouth (smile)
        cv2.ellipse(frame, (center_x, center_y + 40), (50, 30), 
                   0, 0, 180, (100, 50, 50), 3)
    
    return frame


class MindCareDemoNoCamera:
    """Demo mode without camera requirement."""
    
    def __init__(self):
        self.emotion_generator = DemoEmotionGenerator()
        self.time_processor = TimeWindowProcessor(window_size=60)
        self.voice_simulator = VoiceCommandSimulator()
        
        self.is_running = False
        self.is_paused = False
        self.face_present = True
        self.no_face_counter = 0
        
        self.emotion_history = []
        self.start_time = time.time()
        self.frame_count = 0
        self.fps = 0
        self.last_fps_time = time.time()
        
    def draw_emotion_bars(self, frame: np.ndarray, emotion_probs: Dict[str, float], 
                         x: int, y: int, width: int = 200):
        """Draw emotion probability bars."""
        bar_height = 25
        spacing = 5
        
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
        
        cv2.rectangle(frame, (x, y), (x + width, y + height), (40, 40, 40), -1)
        
        fill_width = int(width * fill_pct)
        cv2.rectangle(frame, (x, y), (x + fill_width, y + height), (68, 255, 68), -1)
        
        text = f"Buffer: {fill_pct:.0%}"
        cv2.putText(frame, text, (x + 5, y + 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def draw_stress_meter(self, frame: np.ndarray, valence: float, 
                         x: int, y: int, width: int = 200):
        """Draw stress level meter."""
        height = 30
        
        stress = (1.0 - (valence + 1.0) / 2.0)
        
        cv2.rectangle(frame, (x, y), (x + width, y + height), (40, 40, 40), -1)
        
        fill_width = int(width * stress)
        if stress < 0.3:
            color = (68, 255, 68)
        elif stress < 0.6:
            color = (68, 255, 255)
        else:
            color = (68, 68, 255)
        
        cv2.rectangle(frame, (x, y), (x + fill_width, y + height), color, -1)
        
        text = f"Stress: {stress:.0%}"
        cv2.putText(frame, text, (x + 5, y + 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def draw_voice_command_overlay(self, frame: np.ndarray, command_text: str, 
                                   response: str, progress: float):
        """Draw voice command overlay."""
        h, w = frame.shape[:2]
        
        overlay = frame.copy()
        cv2.rectangle(overlay, (50, h//2 - 100), (w - 50, h//2 + 100), 
                     (30, 30, 30), -1)
        cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
        
        cv2.putText(frame, command_text, (70, h//2 - 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (68, 255, 255), 2)
        
        if progress < 0.3:
            status = "Processing... ⏳"
        elif progress < 0.6:
            status = "Analyzing... 🔍"
        else:
            status = "Response:"
        
        cv2.putText(frame, status, (70, h//2 - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        if progress > 0.5:
            y_offset = h//2 + 20
            for line in response.split('\n'):
                cv2.putText(frame, line, (70, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                y_offset += 30
    
    def draw_help_overlay(self, frame: np.ndarray):
        """Draw help overlay."""
        h, w = frame.shape[:2]
        
        overlay = frame.copy()
        cv2.rectangle(overlay, (w - 280, 10), (w - 10, 250), (30, 30, 30), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        help_text = [
            "CONTROLS:",
            "q - Quit",
            "p - Pause/Resume",
            "h - Toggle help",
            "f - Toggle face",
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
    
    def run(self):
        """Run the demo."""
        self.is_running = True
        show_help = True
        
        print("\n" + "="*60)
        print("MINDCARE DEMO MODE (NO CAMERA)")
        print("="*60)
        print("Using simulated video feed")
        print("Press 'h' to toggle help")
        print("Press 'q' to quit")
        print()
        
        while self.is_running:
            # Create simulated frame
            frame = create_simulated_frame(face_present=self.face_present)
            
            self.frame_count += 1
            
            # Calculate FPS
            current_time = time.time()
            if current_time - self.last_fps_time >= 1.0:
                self.fps = self.frame_count / (current_time - self.last_fps_time)
                self.frame_count = 0
                self.last_fps_time = current_time
            
            # Create display frame
            h, w = frame.shape[:2]
            display = np.zeros((h + 250, w, 3), dtype=np.uint8)
            display[:h, :w] = frame
            
            if not self.is_paused and self.face_present:
                # Generate emotion probabilities
                emotion_probs = self.emotion_generator.get_emotion_probabilities()
                self.time_processor.add_prediction(emotion_probs)
                
                # Get aggregated emotion every second
                if self.frame_count % 30 == 0:
                    aggregated = self.time_processor.get_aggregated_emotion()
                    dominant_emotion = max(aggregated.items(), key=lambda x: x[1])
                    
                    valence = sum(aggregated[e] * VALENCE[e] for e in EMOTIONS)
                    
                    self.emotion_history.append({
                        'emotion': dominant_emotion[0],
                        'confidence': dominant_emotion[1],
                        'valence': valence,
                        'timestamp': datetime.now()
                    })
                
                # Draw face box
                center_x, center_y = w // 2, h // 2
                face_width, face_height = 150, 180
                color = COLORS[self.emotion_generator.current_emotion]
                
                x1 = center_x - face_width - 20
                y1 = center_y - face_height - 20
                x2 = center_x + face_width + 20
                y2 = center_y + face_height + 20
                
                cv2.rectangle(display, (x1, y1), (x2, y2), color, 2)
                
                label = f"{self.emotion_generator.current_emotion.upper()}"
                cv2.putText(display, label, (x1, y1 - 10), 
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
                
            elif not self.face_present:
                cv2.putText(display, "No face detected", (20, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
                cv2.putText(display, "Press 'f' to toggle face", (20, 90), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 1)
            
            # Status bar
            status_y = h + 60
            status_text = f"FPS: {self.fps:.1f} | State: {'PAUSED' if self.is_paused else 'MONITORING'} | Emotions: {len(self.emotion_history)}"
            cv2.putText(display, status_text, (10, status_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Demo mode indicator
            cv2.putText(display, "DEMO MODE (Simulated)", (10, h + 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 255), 1)
            
            # Voice command overlay
            command_info = self.voice_simulator.get_active_command()
            if command_info:
                self.draw_voice_command_overlay(display, *command_info)
            
            # Help overlay
            if show_help:
                self.draw_help_overlay(display)
            
            # Show frame
            cv2.imshow('MindCare Demo (No Camera)', display)
            
            # Handle keyboard input
            key = cv2.waitKey(33) & 0xFF  # ~30 FPS
            
            if key == ord('q'):
                self.is_running = False
            elif key == ord('p'):
                self.is_paused = not self.is_paused
                print(f"{'PAUSED' if self.is_paused else 'RESUMED'}")
            elif key == ord('h'):
                show_help = not show_help
            elif key == ord('f'):
                self.face_present = not self.face_present
                print(f"Face: {'PRESENT' if self.face_present else 'HIDDEN'}")
            elif key in [ord('1'), ord('2'), ord('3'), ord('4')]:
                context = {}
                if self.emotion_history:
                    context['emotion'] = self.emotion_history[-1]['emotion'].upper()
                    context['confidence'] = self.emotion_history[-1]['confidence']
                
                duration = int(time.time() - self.start_time)
                context['duration'] = f"{duration // 60}m {duration % 60}s"
                context['count'] = len(self.emotion_history)
                
                self.voice_simulator.trigger_command(key, context)
                
                if key == ord('2'):
                    self.is_paused = True
                elif key == ord('3'):
                    self.is_paused = False
        
        # Cleanup
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
    print("\n🧠 MindCare Demo - No Camera Version")
    print("This version uses simulated video feed")
    print("Perfect for demonstration without camera permissions!\n")
    
    app = MindCareDemoNoCamera()
    app.run()


if __name__ == "__main__":
    main()
