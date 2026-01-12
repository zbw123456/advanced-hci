"""
Audio Analysis Module for MindCare Demo.
Simulates audio processing since PyAudio dependencies are missing.
Provides waveform generation and audio emotion estimation.
"""

import numpy as np
import random
import time
from collections import deque

class AudioAnalyzer:
    """Simulates real-time audio analysis."""
    
    def __init__(self):
        self.buffer_size = 100
        self.waveform = deque([0.0] * self.buffer_size, maxlen=self.buffer_size)
        self.energy_history = deque([0.0] * 50, maxlen=50)
        self.is_speaking = False
        self.current_audio_emotion = "neutral"
        self.last_update = time.time()
        
    def update(self, is_speaking_simulated=False):
        """
        Update audio state.
        is_speaking_simulated: True if user is pressing a voice command key
        """
        # Generate waveform data
        if is_speaking_simulated:
            # High energy random noise (like speech)
            new_samples = [random.uniform(-0.8, 0.8) for _ in range(5)]
            energy = random.uniform(0.6, 1.0)
            self.is_speaking = True
        else:
            # Low energy background noise
            new_samples = [random.uniform(-0.05, 0.05) for _ in range(5)]
            energy = random.uniform(0.0, 0.1)
            self.is_speaking = False
            
        self.waveform.extend(new_samples)
        self.energy_history.append(energy)
        
        # Periodic estimation update
        if time.time() - self.last_update > 0.5:
            self._estimate_emotion(energy)
            self.last_update = time.time()
            
    def _estimate_emotion(self, current_energy):
        """Estimate emotion based on simulated audio features."""
        if not self.is_speaking:
            self.current_audio_emotion = "silence"
            return

        # Simple heuristic mapping
        if current_energy > 0.8:
            self.current_audio_emotion = random.choice(["angry", "happy", "surprised"])
        elif current_energy > 0.4:
            self.current_audio_emotion = random.choice(["neutral", "happy"])
        else:
            self.current_audio_emotion = random.choice(["sad", "neutral", "calm"])
            
    def get_waveform(self):
        """Return current waveform buffer as list."""
        return list(self.waveform)
    
    def get_current_state(self):
        """Return dict of current audio state."""
        return {
            "emotion": self.current_audio_emotion,
            "energy": self.energy_history[-1],
            "is_speaking": self.is_speaking
        }
