"""
Unit Tests for Security Manager.
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.security import SecurityManager

class TestSecurity(unittest.TestCase):
    def setUp(self):
        # Use a temporary key file
        self.test_key = "test_secret.key"
        self.security = SecurityManager(key_path=self.test_key)

    def tearDown(self):
        # Cleanup
        if os.path.exists(self.test_key):
            os.remove(self.test_key)

    def test_encryption_decryption(self):
        original_text = "Sensitive Patient Data"
        encrypted = self.security.encrypt(original_text)
        
        self.assertNotEqual(original_text, encrypted)
        self.assertIsInstance(encrypted, bytes)
        
        decrypted = self.security.decrypt(encrypted)
        self.assertEqual(original_text, decrypted)

    def test_key_persistence(self):
        # Ensure key remains same if reloaded
        key1 = self.security.key
        
        # New instance pointing to same file
        sec2 = SecurityManager(key_path=self.test_key)
        self.assertEqual(key1, sec2.key)

if __name__ == '__main__':
    unittest.main()
