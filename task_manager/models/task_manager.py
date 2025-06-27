import json
import os
from .task import Task
from datetime import datetime
from task_manager.models.db import db

class TaskManager:
    @staticmethod
    def _get_data_path():
        return os.path.join(os.path.dirname(__file__), '..', 'data', 'tasks.json')

    @staticmethod
    def load_tasks():
        try:
            with open(TaskManager._get_data_path(), "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Task.from_dict(item) for item in data]
        except FileNotFoundError:
            return []

    @staticmethod
    def save_tasks(tasks):
        with open(TaskManager._get_data_path(), "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in tasks], f, indent=4, ensure_ascii=False)

class UserStory(db.Model):
    __tablename__ = 'user_stories'
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    goal = db.Column(db.String(255), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Enum('baja', 'media', 'alta', 'bloqueante'), nullable=False)
    story_points = db.Column(db.Integer, nullable=False)
    effort_hours = db.Column(db.Float, nullable=False)
    prompt = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Relación con Task
    tasks = db.relationship('Task', backref='user_story', lazy=True)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Enum('baja', 'media', 'alta', 'bloqueante'), nullable=False)
    effort_hours = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum('pendiente', 'en progreso', 'en revisión', 'completada'), nullable=False, default='pendiente')
    assigned_to = db.Column(db.String(100), nullable=True)
    user_story_id = db.Column(db.Integer, db.ForeignKey('user_stories.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)