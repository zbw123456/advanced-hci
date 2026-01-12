"""
Unit Tests for Finite State Machine.
"""
import unittest
import sys
import os

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.fsm import FiniteStateMachine, AppState

class TestFSM(unittest.TestCase):
    def setUp(self):
        self.fsm = FiniteStateMachine()

    def test_initial_state(self):
        self.assertEqual(self.fsm.current_state, AppState.START)

    def test_start_monitoring(self):
        self.fsm.start_monitoring()
        self.assertEqual(self.fsm.current_state, AppState.MONITORING)

    def test_pause_resume(self):
        self.fsm.start_monitoring()
        self.fsm.pause()
        self.assertEqual(self.fsm.current_state, AppState.PAUSED)
        self.fsm.resume()
        self.assertEqual(self.fsm.current_state, AppState.MONITORING)

    def test_invalid_transition(self):
        # Cannot pause if not monitoring (e.g. from START)
        self.fsm.pause()
        self.assertEqual(self.fsm.current_state, AppState.START)

if __name__ == '__main__':
    unittest.main()
