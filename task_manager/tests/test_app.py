import unittest
import os
from unittest.mock import patch, MagicMock

# Mock de variables de entorno para la base de datos y modo test
os.environ['DB_USER'] = 'test'
os.environ['DB_PASSWORD'] = 'test'
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_PORT'] = '3306'
os.environ['DB_NAME'] = 'test_db'
os.environ['TESTING'] = '1'

with patch('openai.AzureOpenAI', MagicMock()):
    from task_manager.app import app

class BasicAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_root_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html', response.data)  # Espera HTML de la UI

if __name__ == '__main__':
    unittest.main() 