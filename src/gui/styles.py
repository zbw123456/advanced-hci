"""
QSS Stylesheet for MindCare App.
Implements a Premium Dark Theme.
"""

DARK_THEME = """
QMainWindow {
    background-color: #1e1e1e;
    color: #ffffff;
}

QWidget {
    background-color: #1e1e1e;
    color: #e0e0e0;
    font-family: 'Segoe UI', 'San Francisco', sans-serif;
    font-size: 14px;
}

/* Headers */
QLabel#Header {
    font-size: 20px;
    font-weight: bold;
    color: #ffffff;
    padding: 10px;
}

/* Panels */
QFrame#Panel {
    background-color: #2d2d2d;
    border-radius: 10px;
    border: 1px solid #3d3d3d;
}

/* Buttons */
QPushButton {
    background-color: #0d6efd;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #0b5ed7;
}

QPushButton:pressed {
    background-color: #0a58ca;
}

QPushButton#StopButton {
    background-color: #dc3545;
}

QPushButton#StopButton:hover {
    background-color: #bb2d3b;
}

/* Status Bar */
QStatusBar {
    background-color: #252526;
    color: #aaaaaa;
}

/* Progress Bar (Stress Meter) */
QProgressBar {
    border: 2px solid #3d3d3d;
    border-radius: 5px;
    text-align: center;
    background-color: #2d2d2d;
}

QProgressBar::chunk {
    background-color: #28a745; /* Green by default */
    width: 20px;
}
"""
