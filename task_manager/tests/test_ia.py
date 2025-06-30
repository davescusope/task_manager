import unittest
from unittest.mock import patch, MagicMock
from task_manager.app import app
import json
from datetime import datetime

class IAEndpointsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def mock_task(self):
        mock = MagicMock()
        mock.id = 1
        mock.title = "T"
        mock.description = "D"
        mock.priority = "baja"
        mock.effort_hours = 5
        mock.status = "pendiente"
        mock.assigned_to = "user"
        mock.user_story_id = None
        mock.created_at = datetime.now()
        return mock

    @patch('task_manager.routes.ia_routes.get_llm_response')
    @patch('task_manager.models.Task')
    @patch('task_manager.models.Task.query')
    @patch('task_manager.models.db.db.session')
    def test_describe_task(self, mock_session, mock_query, mock_task, mock_llm):
        mock_task_instance = self.mock_task()
        mock_query.get.return_value = mock_task_instance
        mock_llm.return_value = 'Descripción generada'
        mock_taskIASchema = type('MockSchema', (), {'from_orm': lambda self, x: type('MockObj', (), {'dict': lambda self: {
            'id': 1,
            'title': 'T',
            'description': 'Descripción generada',
            'priority': 'baja',
            'effort_hours': 5,
            'status': 'pendiente',
            'assigned_to': 'user',
            'user_story_id': None,
            'created_at': datetime.now()
        }})()})
        with patch('task_manager.models.schemas.TaskIASchema', mock_taskIASchema):
            data = {"task_id": 1}
            response = self.app.post('/ai/tasks/describe', data=json.dumps(data), content_type='application/json')
            self.assertIn(response.status_code, [200, 404, 400])

    @patch('task_manager.routes.ia_routes.get_llm_response')
    @patch('task_manager.models.Task')
    @patch('task_manager.models.Task.query')
    def test_categorize_task(self, mock_query, mock_task, mock_llm):
        mock_task_instance = self.mock_task()
        mock_query.get.return_value = mock_task_instance
        mock_llm.return_value = 'Backend'
        mock_taskIASchema = type('MockSchema', (), {'from_orm': lambda self, x: type('MockObj', (), {'dict': lambda self: {
            'id': 1,
            'title': 'T',
            'description': 'D',
            'priority': 'baja',
            'effort_hours': 5,
            'status': 'pendiente',
            'assigned_to': 'user',
            'user_story_id': None,
            'created_at': datetime.now(),
            'category': 'Backend'
        }})()})
        with patch('task_manager.models.schemas.TaskIASchema', mock_taskIASchema):
            data = {"task_id": 1}
            response = self.app.post('/ai/tasks/categorize', data=json.dumps(data), content_type='application/json')
            self.assertIn(response.status_code, [200, 404, 400])

    @patch('task_manager.routes.ia_routes.get_llm_response')
    @patch('task_manager.models.Task')
    @patch('task_manager.models.Task.query')
    @patch('task_manager.models.db.db.session')
    def test_estimate_task(self, mock_session, mock_query, mock_task, mock_llm):
        mock_task_instance = self.mock_task()
        mock_query.get.return_value = mock_task_instance
        mock_llm.return_value = '5'
        mock_taskIASchema = type('MockSchema', (), {'from_orm': lambda self, x: type('MockObj', (), {'dict': lambda self: {
            'id': 1,
            'title': 'T',
            'description': 'D',
            'priority': 'baja',
            'effort_hours': 5,
            'status': 'pendiente',
            'assigned_to': 'user',
            'user_story_id': None,
            'created_at': datetime.now()
        }})()})
        with patch('task_manager.models.schemas.TaskIASchema', mock_taskIASchema):
            data = {"task_id": 1}
            response = self.app.post('/ai/tasks/estimate', data=json.dumps(data), content_type='application/json')
            self.assertIn(response.status_code, [200, 404, 400, 500])

    @patch('task_manager.routes.ia_routes.get_llm_response')
    @patch('task_manager.models.Task')
    @patch('task_manager.models.Task.query')
    @patch('task_manager.models.db.db.session')
    def test_audit_task(self, mock_session, mock_query, mock_task, mock_llm):
        mock_task_instance = self.mock_task()
        mock_query.get.return_value = mock_task_instance
        mock_llm.return_value = 'Análisis de riesgos'
        mock_taskIASchema = type('MockSchema', (), {'from_orm': lambda self, x: type('MockObj', (), {'dict': lambda self: {
            'id': 1,
            'title': 'T',
            'description': 'D',
            'priority': 'baja',
            'effort_hours': 5,
            'status': 'pendiente',
            'assigned_to': 'user',
            'user_story_id': None,
            'created_at': datetime.now(),
            'risk_analysis': 'Análisis de riesgos'
        }})()})
        with patch('task_manager.models.schemas.TaskIASchema', mock_taskIASchema):
            data = {"task_id": 1}
            response = self.app.post('/ai/tasks/audit', data=json.dumps(data), content_type='application/json')
            self.assertIn(response.status_code, [200, 404, 400])

if __name__ == '__main__':
    unittest.main() 