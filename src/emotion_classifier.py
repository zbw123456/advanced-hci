"""
Emotion classification module using CNN.
Classifies facial expressions into emotion categories.
"""

import numpy as np
import cv2
from typing import Dict, Optional
import tensorflow as tf
from tensorflow import keras
import config


class EmotionClassifier:
    """Classifies facial expressions using a pre-trained CNN model."""
    
    def __init__(self, model_path: str = None):
        """
        Initialize emotion classifier.
        
        Args:
            model_path: Path to pre-trained model file (.h5)
        """
        self.model = None
        self.model_path = model_path or str(config.MODEL_PATH)
        
        # Try to load model if it exists
        if config.MODEL_PATH.exists():
            try:
                self.model = keras.models.load_model(self.model_path)
                print(f"Loaded emotion model from {self.model_path}")
            except Exception as e:
                print(f"Error loading model: {e}")
                print("Will use simple demo model instead")
                self.model = None
        
        # If no model available, create a simple demo model
        # In a real implementation, you would train or download a proper model
        if self.model is None:
            print("Creating demo emotion model...")
            self.model = self._create_demo_model()
    
    def _create_demo_model(self) -> keras.Model:
        """
        Create a simple demo CNN model for emotion classification.
        This is a placeholder - in production, use a properly trained model.
        
        Returns:
            Keras model
        """
        model = keras.Sequential([
            keras.layers.Input(shape=(*config.MODEL_INPUT_SIZE, 1)),
            
            keras.layers.Conv2D(32, (3, 3), activation='relu'),
            keras.layers.BatchNormalization(),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Dropout(0.25),
            
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.BatchNormalization(),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Dropout(0.25),
            
            keras.layers.Conv2D(128, (3, 3), activation='relu'),
            keras.layers.BatchNormalization(),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Dropout(0.25),
            
            keras.layers.Flatten(),
            keras.layers.Dense(256, activation='relu'),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(len(config.EMOTION_LABELS), activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # NOTE: This demo model is NOT trained and will give random predictions
        # For actual use, you need to:
        # 1. Download a pre-trained model (e.g., from https://github.com/oarriaga/face_classification)
        # 2. Train your own model on FER-2013 or similar dataset
        
        print("⚠️  WARNING: Using untrained demo model - predictions will be random!")
        print("   For real use, download a pre-trained model or train your own.")
        
        return model
    
    def preprocess_face(self, face_img: np.ndarray) -> np.ndarray:
        """
        Preprocess face image for model input.
        
        Args:
            face_img: Face image (can be color or grayscale)
            
        Returns:
            Preprocessed image ready for model
        """
        # Convert to grayscale if needed
        if len(face_img.shape) == 3:
            face_gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        else:
            face_gray = face_img
        
        # Resize to model input size
        face_resized = cv2.resize(face_gray, config.MODEL_INPUT_SIZE)
        
        # Normalize pixel values to [0, 1]
        face_normalized = face_resized.astype('float32') / 255.0
        
        # Add channel dimension (grayscale has 1 channel)
        face_final = np.expand_dims(face_normalized, axis=-1)
        
        # Add batch dimension
        face_batch = np.expand_dims(face_final, axis=0)
        
        return face_batch
    
    def classify_emotion(self, face_img: np.ndarray) -> Dict[str, float]:
        """
        Classify emotion in a face image.
        
        Args:
            face_img: Face image (BGR or grayscale)
            
        Returns:
            Dictionary with emotion labels as keys and probabilities as values
        """
        # Preprocess image
        preprocessed = self.preprocess_face(face_img)
        
        # Get model predictions
        predictions = self.model.predict(preprocessed, verbose=0)[0]
        
        # Create emotion dictionary
        emotion_probs = {
            emotion: float(prob) 
            for emotion, prob in zip(config.EMOTION_LABELS, predictions)
        }
        
        return emotion_probs
    
    def get_dominant_emotion(self, emotion_probs: Dict[str, float]) -> tuple:
        """
        Get the emotion with highest probability.
        
        Args:
            emotion_probs: Dictionary of emotion probabilities
            
        Returns:
            Tuple (emotion_label, confidence)
        """
        dominant_emotion = max(emotion_probs.items(), key=lambda x: x[1])
        return dominant_emotion
    
    def calculate_valence_arousal(self, emotion_probs: Dict[str, float]) -> tuple:
        """
        Calculate valence and arousal from emotion probabilities.
        
        Args:
            emotion_probs: Dictionary of emotion probabilities
            
        Returns:
            Tuple (valence, arousal) in range [-1, 1]
        """
        valence = sum(
            emotion_probs[emotion] * config.EMOTION_VALENCE[emotion]
            for emotion in config.EMOTION_LABELS
        )
        
        arousal = sum(
            emotion_probs[emotion] * config.EMOTION_AROUSAL[emotion]
            for emotion in config.EMOTION_LABELS
        )
        
        return valence, arousal


class TimeWindowProcessor:
    """
    Processes emotion predictions over time windows.
    Implements sliding window aggregation to smooth predictions.
    """
    
    def __init__(self, window_size: int = config.FRAME_BUFFER_SIZE):
        """
        Initialize time window processor.
        
        Args:
            window_size: Number of frames to aggregate
        """
        self.window_size = window_size
        self.emotion_buffer = []
        self.timestamp_buffer = []
    
    def add_prediction(self, emotion_probs: Dict[str, float], timestamp: float):
        """
        Add an emotion prediction to the buffer.
        
        Args:
            emotion_probs: Dictionary of emotion probabilities
            timestamp: Timestamp of the prediction
        """
        self.emotion_buffer.append(emotion_probs)
        self.timestamp_buffer.append(timestamp)
        
        # Remove oldest if buffer exceeds window size
        if len(self.emotion_buffer) > self.window_size:
            self.emotion_buffer.pop(0)
            self.timestamp_buffer.pop(0)
    
    def get_aggregated_emotion(self) -> Optional[Dict[str, float]]:
        """
        Get aggregated emotion over the time window.
        Uses weighted average of all predictions in the buffer.
        
        Returns:
            Aggregated emotion probabilities, or None if buffer empty
        """
        if not self.emotion_buffer:
            return None
        
        # Calculate average probabilities across all frames in window
        aggregated = {emotion: 0.0 for emotion in config.EMOTION_LABELS}
        
        for emotion_probs in self.emotion_buffer:
            for emotion, prob in emotion_probs.items():
                aggregated[emotion] += prob
        
        # Normalize by number of frames
        num_frames = len(self.emotion_buffer)
        for emotion in aggregated:
            aggregated[emotion] /= num_frames
        
        return aggregated
    
    def get_dominant_emotion_majority(self) -> Optional[str]:
        """
        Get dominant emotion using majority voting.
        
        Returns:
            Most frequent emotion label, or None if buffer empty
        """
        if not self.emotion_buffer:
            return None
        
        # Get dominant emotion for each frame
        dominant_emotions = [
            max(probs.items(), key=lambda x: x[1])[0]
            for probs in self.emotion_buffer
        ]
        
        # Return most common
        return max(set(dominant_emotions), key=dominant_emotions.count)
    
    def clear(self):
        """Clear the buffer."""
        self.emotion_buffer.clear()
        self.timestamp_buffer.clear()
