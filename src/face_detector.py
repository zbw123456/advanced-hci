"""
Face detection module using OpenCV.
Detects faces in video frames and extracts face regions.
"""

import cv2
import numpy as np
from typing import Optional, Tuple
import config


class FaceDetector:
    """Detects faces in images using Haar Cascade or DNN."""
    
    def __init__(self, method='haar'):
        """
        Initialize face detector.
        
        Args:
            method: 'haar' for Haar Cascade or 'dnn' for DNN-based detection
        """
        self.method = method
        
        if method == 'haar':
            # Load Haar Cascade classifier
            cascade_path = cv2.data.haarcascades + config.FACE_CASCADE_PATH
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            
            if self.face_cascade.empty():
                raise FileNotFoundError(f"Haar cascade file not found: {cascade_path}")
                
        elif method == 'dnn':
            # Load DNN model (optional, more accurate but slower)
            # Using OpenCV's pre-trained face detector
            model_file = "res10_300x300_ssd_iter_140000.caffemodel"
            config_file = "deploy.prototxt"
            # Note: These files would need to be downloaded separately
            # For this implementation, we'll primarily use Haar Cascade
            raise NotImplementedError("DNN method requires model files to be downloaded")
        
        self.last_face_time = None
        
    def detect_face(self, frame: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """
        Detect the largest face in the frame.
        
        Args:
            frame: Input image (BGR format)
            
        Returns:
            Tuple (x, y, w, h) of the largest face bounding box, or None if no face found
        """
        # Convert to grayscale for Haar Cascade
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=config.SCALE_FACTOR,
            minNeighbors=config.MIN_NEIGHBORS,
            minSize=config.MIN_FACE_SIZE
        )
        
        if len(faces) == 0:
            return None
        
        # Return the largest face (by area)
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        return tuple(largest_face)
    
    def extract_face_region(self, frame: np.ndarray, bbox: Tuple[int, int, int, int],
                           target_size: Tuple[int, int] = None) -> np.ndarray:
        """
        Extract and preprocess face region from frame.
        
        Args:
            frame: Input image
            bbox: Bounding box (x, y, w, h)
            target_size: Resize to this size (for model input)
            
        Returns:
            Processed face image
        """
        x, y, w, h = bbox
        
        # Extract face region
        face = frame[y:y+h, x:x+w]
        
        # Resize if target size specified
        if target_size:
            face = cv2.resize(face, target_size)
        
        return face
    
    def draw_face_box(self, frame: np.ndarray, bbox: Tuple[int, int, int, int],
                     label: str = None, color: Tuple[int, int, int] = (0, 255, 0)) -> np.ndarray:
        """
        Draw bounding box around detected face.
        
        Args:
            frame: Input image
            bbox: Bounding box (x, y, w, h)
            label: Optional text label to display
            color: Box color in BGR
            
        Returns:
            Frame with drawn box
        """
        x, y, w, h = bbox
        
        # Draw rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        
        # Draw label if provided
        if label:
            # Background for text
            (text_width, text_height), _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
            )
            cv2.rectangle(
                frame, 
                (x, y - text_height - 10), 
                (x + text_width, y), 
                color, 
                -1
            )
            # Text
            cv2.putText(
                frame, 
                label, 
                (x, y - 5), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.6, 
                (255, 255, 255), 
                2
            )
        
        return frame


class CameraManager:
    """Manages camera access and frame capture."""
    
    def __init__(self, camera_index: int = config.CAMERA_INDEX):
        """
        Initialize camera.
        
        Args:
            camera_index: Camera device index (0 for default)
        """
        self.camera_index = camera_index
        self.cap = None
        self.is_open = False
        
    def open(self) -> bool:
        """
        Open camera connection.
        
        Returns:
            True if successful, False otherwise
        """
        self.cap = cv2.VideoCapture(self.camera_index)
        
        if not self.cap.isOpened():
            return False
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, config.CAMERA_FPS)
        
        self.is_open = True
        return True
    
    def read_frame(self) -> Optional[np.ndarray]:
        """
        Read a frame from the camera.
        
        Returns:
            Frame as numpy array, or None if read failed
        """
        if not self.is_open or self.cap is None:
            return None
        
        ret, frame = self.cap.read()
        
        if not ret:
            return None
        
        return frame
    
    def close(self):
        """Release camera resources."""
        if self.cap is not None:
            self.cap.release()
            self.is_open = False
    
    def __enter__(self):
        """Context manager entry."""
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
