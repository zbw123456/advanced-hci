"""
Standalone Audio Emotion Recognition Demo.
Focuses purely on the audio modality of the MindCare system.
Simulates real-time audio waveform analysis and emotion classification.
"""

import cv2
import numpy as np
import time
from audio_module import AudioAnalyzer

class AudioDemoApp:
    def __init__(self):
        self.audio_analyzer = AudioAnalyzer()
        self.width = 800
        self.height = 400
        self.is_running = True
        self.active_emotion = None
        self.emotion_timer = 0
        
        # Color scheme matches main demo
        self.colors = {
            'angry': (68, 68, 255),      # Red
            'disgusted': (255, 68, 170),  # Purple
            'fearful': (68, 153, 255),    # Orange
            'happy': (68, 255, 68),       # Green
            'sad': (255, 68, 68),         # Blue
            'surprised': (68, 255, 255),  # Yellow
            'neutral': (255, 255, 255),   # White
            'silence': (100, 100, 100)    # Gray
        }

    def run(self):
        print("\n🎤 MindCare Audio Analysis Demo")
        print("-------------------------------")
        print("Press '1': Simulate HAPPY speech")
        print("Press '2': Simulate ANGRY speech")
        print("Press '3': Simulate SAD speech")
        print("Press '4': Simulate NEUTRAL speech")
        print("Press 'q': Quit")
        
        while self.is_running:
            # Update state
            is_speaking = False
            
            # Handle simulated speech duration
            if self.active_emotion and time.time() - self.emotion_timer < 2.0:
                is_speaking = True
                # Start new logic to override analyzer for demo control
                self.audio_analyzer.current_audio_emotion = self.active_emotion
            else:
                self.active_emotion = None

            self.audio_analyzer.update(is_speaking)
            
            # Draw UI
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            
            # Title
            cv2.putText(frame, "AUDIO EMOTION RECOGNITION", (20, 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)

            # Waveform
            waveform = self.audio_analyzer.get_waveform()
            if waveform:
                center_y = self.height // 2
                points = []
                for i, val in enumerate(waveform):
                    px = int(50 + (i / len(waveform)) * (self.width - 100))
                    # Amplify height for better visual
                    py = int(center_y + val * 100) 
                    points.append((px, py))
                
                if len(points) > 1:
                    cv2.polylines(frame, [np.array(points)], False, (0, 255, 255), 2)

            # Get state
            audio_state = self.audio_analyzer.get_current_state()
            
            # Display logic
            current_emotion = audio_state["emotion"]
            if self.active_emotion:
                current_emotion = self.active_emotion

            # Emotion Display
            color = self.colors.get(current_emotion, (200, 200, 200))
            text = f"EMOTION: {current_emotion.upper()}"
            
            # Center text
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)[0]
            text_x = (self.width - text_size[0]) // 2
            
            cv2.putText(frame, text, (text_x, self.height - 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)

            # Controls Help
            cv2.putText(frame, "Controls: 1 (Happy), 2 (Angry), 3 (Sad), 4 (Neutral), Q (Quit)", (20, self.height - 15), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 150, 150), 1)

            cv2.imshow("Audio Analysis Demo", frame)
            
            # Input handling
            key = cv2.waitKey(30) & 0xFF
            if key == ord('q'):
                self.is_running = False
            elif key == ord('1'):
                self.active_emotion = "happy"
                self.emotion_timer = time.time()
            elif key == ord('2'):
                self.active_emotion = "angry"
                self.emotion_timer = time.time()
            elif key == ord('3'):
                self.active_emotion = "sad"
                self.emotion_timer = time.time()
            elif key == ord('4'):
                self.active_emotion = "neutral"
                self.emotion_timer = time.time()

        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = AudioDemoApp()
    app.run()
