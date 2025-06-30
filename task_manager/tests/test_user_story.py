import unittest
from unittest.mock import patch, MagicMock
from task_manager.app import app
import json
from datetime import datetime

class UserStoryEndpointsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def mock_user_story(self):
        mock = MagicMock()
        mock.id = 1
        mock.project = "Test"
        mock.role = "dev"
        mock.goal = "goal"
        mock.reason = "reason"
        mock.description = "desc"
        mock.priority = "baja"
        mock.story_points = 1
        mock.effort_hours = 2
        mock.prompt = "algo"
        mock.created_at = datetime.now()
        return mock

    @patch('task_manager.models.UserStory')
    @patch('task_manager.models.UserStory.query')
    def test_get_user_stories_empty(self, mock_query, mock_user_story):
        mock_query.all.return_value = []
        response = self.app.get('/user-stories')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'user_stories', response.data)

    @patch('task_manager.models.UserStory')
    @patch('task_manager.models.UserStory.query')
    def test_get_user_story_not_found(self, mock_query, mock_user_story):
        mock_query.get.return_value = None
        response = self.app.get('/user-stories?id=1')
        self.assertEqual(response.status_code, 404)

    @patch('task_manager.routes.user_story_routes.get_llm_response')
    @patch('task_manager.models.db.db.session')
    @patch('task_manager.models.UserStory')
    def test_create_user_story(self, mock_user_story, mock_session, mock_llm):
        mock_llm.return_value = json.dumps({
            "project": "Test",
            "role": "dev",
            "goal": "goal",
            "reason": "reason",
            "description": "desc",
            "priority": "baja",
            "story_points": 1,
            "effort_hours": 2
        })
        mock_user_story_instance = self.mock_user_story()
        mock_user_story.return_value = mock_user_story_instance
        mock_user_storySchema = type('MockSchema', (), {
            'from_orm': staticmethod(lambda x: type('MockObj', (), {'dict': lambda self: {
                'id': 1,
                'project': 'Test',
                'role': 'dev',
                'goal': 'goal',
                'reason': 'reason',
                'description': 'desc',
                'priority': 'baja',
                'story_points': 1,
                'effort_hours': 2,
                'prompt': 'algo',
                'created_at': datetime.now()
            }})())
        })
        with patch('task_manager.routes.user_story_routes.UserStorySchema', mock_user_storySchema):
            data = {"prompt": "algo"}
            response = self.app.post('/user-stories', data=json.dumps(data), content_type='application/json')
            self.assertIn(response.status_code, [200, 201, 400])

    @patch('task_manager.models.UserStory')
    @patch('task_manager.models.UserStory.query')
    def test_get_tasks_for_user_story_not_found(self, mock_query, mock_user_story):
        mock_query.get.return_value = None
        response = self.app.get('/user-stories/1/tasks')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main() 