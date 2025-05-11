# tests/test_messagegen.py

import unittest
from core.messagegen_ai_v2 import MessageGeneratorAI

class TestMessageGeneratorAI(unittest.TestCase):
    def test_generar_mensaje(self):
        db = None  # Mock or actual database connection
        generator = MessageGeneratorAI(db)
        lead = {
            "name": "John Doe",
            "company": "TechCorp",
            "industry": "Technology",
            "position": "CTO"
        }
        message = generator.generar_mensaje(lead)
        self.assertIn("John Doe", message)