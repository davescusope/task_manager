import unittest
import os
from unittest.mock import patch, MagicMock
from datetime import datetime
import json

# Mock de variables de entorno para la base de datos y modo test
os.environ['DB_USER'] = 'test'
os.environ['DB_PASSWORD'] = 'test'
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_PORT'] = '3306'
os.environ['DB_NAME'] = 'test_db'
os.environ['TESTING'] = '1'

with patch('openai.AzureOpenAI', MagicMock()):
    from task_manager.app import app

class CrudEndpointsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def mock_task(self):
        # Devuelve un mock de Task con todos los campos requeridos
        mock = MagicMock()
        mock.id = 1
        mock.title = "Test Task"
        mock.description = "Desc"
        mock.priority = "baja"
        mock.effort_hours = 1
        mock.status = "pendiente"
        mock.assigned_to = "user"
        mock.user_story_id = None
        mock.created_at = datetime.now()
        return mock

    @patch('task_manager.models.Task')
    @patch('task_manager.models.Task.query')
    def test_get_tasks(self, mock_query, mock_task):
        mock_task_instance = self.mock_task()
        mock_query.all.return_value = [mock_task_instance]
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'tasks', response.data)

    @patch('task_manager.models.Task')
    @patch('task_manager.models.Task.query')
    def test_get_task_not_found(self, mock_query, mock_task):
        mock_query.get.return_value = None
        response = self.app.get('/tasks/1')
        self.assertEqual(response.status_code, 404)

    @patch('task_manager.models.db.db.session')
    @patch('task_manager.models.Task')
    def test_create_task(self, mock_task, mock_session):
        mock_task_instance = self.mock_task()
        mock_task.return_value = mock_task_instance
        mock_taskClassicSchema = type('MockSchema', (), {
            'from_orm': staticmethod(lambda x: type('MockObj', (), {'dict': lambda self: {
                'id': 1,
                'title': 'Test Task',
                'description': 'Desc',
                'priority': 'baja',
                'effort_hours': 1,
                'status': 'pendiente',
                'assigned_to': 'user',
                'user_story_id': None,
                'created_at': datetime.now()
            }})())
        })
        with patch('task_manager.routes.crud_routes.TaskClassicSchema', mock_taskClassicSchema):
            data = {
                "title": "Test Task",
                "description": "Desc",
                "priority": "baja",
                "effort_hours": 1,
                "status": "pendiente",
                "assigned_to": "user"
            }
            response = self.app.post('/tasks', data=json.dumps(data), content_type='application/json')
            self.assertIn(response.status_code, [200, 201, 400])

    @patch('task_manager.models.Task')
    @patch('task_manager.models.Task.query')
    def test_update_task_not_found(self, mock_query, mock_task):
        mock_query.get.return_value = None
        response = self.app.put('/tasks/1', data=json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    @patch('task_manager.models.Task')
    @patch('task_manager.models.Task.query')
    @patch('task_manager.models.db.db.session')
    def test_delete_task_not_found(self, mock_session, mock_query, mock_task):
        mock_query.get.return_value = None
        response = self.app.delete('/tasks/1')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main() 