import unittest
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