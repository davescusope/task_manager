from flask import Blueprint, request, jsonify
from task_manager.models import UserStory, Task
from task_manager.models.db import db
from task_manager.models.schemas import UserStorySchema, UserStorySchemas, TaskWithUserStorySchema
from ..connection.connection import API_KEY, API_BASE, API_VERSION, MODEL_NAME
from openai import AzureOpenAI

client = AzureOpenAI(
    api_version=API_VERSION,
    azure_endpoint=API_BASE,
    api_key=API_KEY,
)

def get_llm_response(system_prompt, user_prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    response = client.chat.completions.create(
        messages=messages,
        max_tokens=500,
        temperature=0.7,
        top_p=1.0,
        model=MODEL_NAME
    )
    return response.choices[0].message.content

user_story_bp = Blueprint("user_story", __name__)

@user_story_bp.route('/user-stories', methods=['GET'])
def get_user_stories():
    user_story_id = request.args.get('id', type=int)
    if user_story_id:
        user_story = UserStory.query.get(user_story_id)
        if not user_story:
            return jsonify({'error': 'User story not found'}), 404
        result = UserStorySchema.from_orm(user_story)
        return jsonify(result.dict())
    else:
        user_stories = UserStory.query.all()
        result = UserStorySchemas(user_stories=[UserStorySchema.from_orm(us) for us in user_stories])
        return jsonify(result.dict())

@user_story_bp.route('/user-stories', methods=['POST'])
def create_user_story():
    data = request.json or request.form
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    system_prompt = (
        "Eres un experto en análisis de requisitos. "
        "Genera una historia de usuario estructurada en JSON puro (sin explicaciones, sin markdown, sin comentarios) "
        "con los campos: project, role, goal, reason, description, priority, story_points, effort_hours. "
        "El campo 'priority' debe ser SOLO uno de estos valores en minúsculas y en español: 'baja', 'media', 'alta', 'bloqueante'. "
        "Devuelve SOLO el objeto JSON."
    )
    user_prompt = prompt
    response = get_llm_response(system_prompt, user_prompt)
    import json as pyjson
    raw = response.strip()
    if raw.startswith('```'):
        raw = raw.split('\n', 1)[-1]
        if raw.endswith('```'):
            raw = raw.rsplit('```', 1)[0]
        if raw.lower().startswith('json'):
            raw = raw[4:].lstrip('\n')
    try:
        story_data = pyjson.loads(raw)
    except Exception:
        return jsonify({'error': 'Respuesta IA no válida', 'raw': response}), 500
    prioridad_valida = {'baja', 'media', 'alta', 'bloqueante'}
    if story_data['priority'].lower() not in prioridad_valida:
        return jsonify({'error': f"Valor de prioridad inválido: '{story_data['priority']}'. Debe ser uno de: baja, media, alta, bloqueante.", 'raw': story_data}), 400
    user_story = UserStory(
        project=story_data['project'],
        role=story_data['role'],
        goal=story_data['goal'],
        reason=story_data['reason'],
        description=story_data['description'],
        priority=story_data['priority'].lower(),
        story_points=story_data['story_points'],
        effort_hours=story_data['effort_hours'],
        prompt=prompt
    )
    db.session.add(user_story)
    db.session.commit()
    return jsonify(UserStorySchema.from_orm(user_story).dict()), 201

@user_story_bp.route('/user-stories/<int:user_story_id>/generate-tasks', methods=['POST'])
def generate_tasks_for_user_story(user_story_id):
    user_story = UserStory.query.get(user_story_id)
    if not user_story:
        return jsonify({'error': 'User story not found'}), 404
    system_prompt = (
        "Eres un experto en gestión de proyectos. "
        "Genera una lista de máximo 5 tareas en JSON puro (sin explicaciones, sin markdown, sin comentarios) para la siguiente historia de usuario. "
        "Cada tarea debe tener los campos: title, description, priority, effort_hours, status, assigned_to. "
        "El campo 'priority' debe ser SOLO uno de estos valores en minúsculas y en español: 'baja', 'media', 'alta', 'bloqueante'. "
        "El campo 'status' debe ser SOLO uno de estos valores en minúsculas y en español: 'pendiente', 'en progreso', 'en revisión', 'completada'. "
        "Devuelve SOLO un array JSON de objetos tarea."
    )
    user_prompt = f"Historia de usuario: {user_story.description}"
    response = get_llm_response(system_prompt, user_prompt)
    import json as pyjson
    raw = response.strip()
    if raw.startswith('```'):
        raw = raw.split('\n', 1)[-1]
        if raw.endswith('```'):
            raw = raw.rsplit('```', 1)[0]
        if raw.lower().startswith('json'):
            raw = raw[4:].lstrip('\n')
    try:
        tasks_data = pyjson.loads(raw)
    except Exception:
        return jsonify({'error': 'Respuesta IA no válida', 'raw': response}), 500
    prioridad_valida = {'baja', 'media', 'alta', 'bloqueante'}
    status_valido = {'pendiente', 'en progreso', 'en revisión', 'completada'}
    created_tasks = []
    for t in tasks_data:
        if t['priority'].lower() not in prioridad_valida or t['status'].lower() not in status_valido:
            continue
        task = Task(
            title=t['title'],
            description=t['description'],
            priority=t['priority'].lower(),
            effort_hours=t['effort_hours'],
            status=t['status'].lower(),
            assigned_to=t['assigned_to'],
            user_story_id=user_story_id
        )
        db.session.add(task)
        created_tasks.append(task)
    db.session.commit()
    return jsonify({'tasks': [TaskWithUserStorySchema.from_orm(task).dict() for task in created_tasks]}), 201

@user_story_bp.route('/user-stories/<int:user_story_id>/tasks', methods=['GET'])
def get_tasks_for_user_story(user_story_id):
    user_story = UserStory.query.get(user_story_id)
    if not user_story:
        return jsonify({'error': 'User story not found'}), 404
    tasks = Task.query.filter_by(user_story_id=user_story_id).all()
    result = {'tasks': [TaskWithUserStorySchema.from_orm(task).dict() for task in tasks]}
    return jsonify(result) 