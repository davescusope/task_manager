from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# --- CRUD clásico de tareas ---
class TaskClassicSchema(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    effort_hours: float
    status: str
    assigned_to: Optional[str]
    user_story_id: Optional[int] = None
    created_at: datetime
    class Config:
        from_attributes = True

# --- IA sobre tareas ---
class TaskIASchema(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    effort_hours: float
    status: str
    assigned_to: Optional[str]
    created_at: datetime
    # Puedes añadir campos IA si los necesitas
    class Config:
        from_attributes = True

# --- Tareas asociadas a historias de usuario ---
class TaskWithUserStorySchema(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    effort_hours: float
    status: str
    assigned_to: Optional[str]
    user_story_id: int
    created_at: datetime
    class Config:
        from_attributes = True

class UserStorySchema(BaseModel):
    id: int
    project: str
    role: str
    goal: str
    reason: str
    description: str
    priority: str
    story_points: int
    effort_hours: float
    prompt: str | None = None
    created_at: datetime
    tasks: Optional[List[TaskWithUserStorySchema]] = []
    class Config:
        from_attributes = True

class UserStorySchemas(BaseModel):
    user_stories: List[UserStorySchema] 