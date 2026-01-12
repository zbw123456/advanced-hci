"""
Finite State Machine for MindCare System.
"""
from enum import Enum, auto

class AppState(Enum):
    START = auto()
    MONITORING = auto()
    PAUSED = auto()
    ALERT = auto()
    STOPPED = auto()

class FiniteStateMachine:
    def __init__(self):
        self.current_state = AppState.START
        self.history = []
        
    def transition_to(self, new_state: AppState):
        """Execute state transition if valid."""
        # Simple validation for now
        print(f"FSM: Transitioning from {self.current_state.name} to {new_state.name}")
        self.history.append(self.current_state)
        self.current_state = new_state
        return True

    def start_monitoring(self):
        if self.current_state in [AppState.START, AppState.STOPPED, AppState.PAUSED]:
            self.transition_to(AppState.MONITORING)
            
    def pause(self):
        if self.current_state == AppState.MONITORING:
            self.transition_to(AppState.PAUSED)
            
    def resume(self):
        if self.current_state == AppState.PAUSED:
            self.transition_to(AppState.MONITORING)
            
    def trigger_alert(self):
        if self.current_state == AppState.MONITORING:
            self.transition_to(AppState.ALERT)
            
    def resolve_alert(self):
        if self.current_state == AppState.ALERT:
            self.transition_to(AppState.MONITORING)
            
    def stop(self):
        self.transition_to(AppState.STOPPED)
