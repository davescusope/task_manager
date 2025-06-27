from flask import Blueprint, request, jsonify
from openai import AzureOpenAI
from task_manager.models import Task
from task_manager.models.db import db
from task_manager.models.schemas import TaskIASchema
from ..connection.connection import API_KEY, API_BASE, API_VERSION, MODEL_NAME

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

ia_bp = Blueprint("ia", __name__)

@ia_bp.route("/ai/tasks/describe", methods=["POST"])
def describe_task():
    data = request.json
    if not data.get("task_id"):
        return jsonify({"error": "task_id is required"}), 400
    task = Task.query.get(data["task_id"])
    if not task:
        return jsonify({"error": "Task not found"}), 404
    system_prompt = "Eres un experto en gestión de tareas. Tu tarea es generar una descripción detallada y profesional para una tarea basándote en su título y otros campos disponibles. La descripción debe ser clara, muy concisa y útil para entender el alcance y objetivos de la tarea."
    user_prompt = f"Genera una descripción detallada pero muy muy concisa para la siguiente tarea:\nTítulo: {task.title}\n"
    if task.priority:
        user_prompt += f"Prioridad: {task.priority}\n"
    if task.status:
        user_prompt += f"Estado: {task.status}\n"
    if task.assigned_to:
        user_prompt += f"Asignado a: {task.assigned_to}\n"
    description = get_llm_response(system_prompt, user_prompt)
    task.description = description
    db.session.commit()
    return jsonify(TaskIASchema.from_orm(task).dict())

@ia_bp.route("/ai/tasks/categorize", methods=["POST"])
def categorize_task():
    data = request.json
    if not data.get("task_id"):
        return jsonify({"error": "task_id is required"}), 400
    task = Task.query.get(data["task_id"])
    if not task:
        return jsonify({"error": "Task not found"}), 404
    system_prompt = "Eres un experto en categorización de tareas de desarrollo de software. Tu tarea es clasificar la tarea en una de las siguientes categorías: Frontend, Backend, Testing, Infra, o DevOps. Responde ÚNICAMENTE con el nombre de la categoría, sin explicaciones adicionales."
    user_prompt = f"Categoriza la siguiente tarea:\nTítulo: {task.title}\n"
    if task.description:
        user_prompt += f"Descripción: {task.description}\n"
    category = get_llm_response(system_prompt, user_prompt).strip()
    return jsonify({"category": category, **TaskIASchema.from_orm(task).dict()})

@ia_bp.route("/ai/tasks/estimate", methods=["POST"])
def estimate_task():
    data = request.json
    if not data.get("task_id"):
        return jsonify({"error": "task_id is required"}), 400
    task = Task.query.get(data["task_id"])
    if not task:
        return jsonify({"error": "Task not found"}), 404
    system_prompt = "Eres un experto en estimación de esfuerzo para tareas de desarrollo de software. Tu tarea es estimar el número de horas que tomará completar la tarea. Responde ÚNICAMENTE con un número entero o decimal, sin explicaciones adicionales."
    user_prompt = f"Estima el esfuerzo en horas para la siguiente tarea:\nTítulo: {task.title}\n"
    if task.description:
        user_prompt += f"Descripción: {task.description}\n"
    try:
        effort_hours = float(get_llm_response(system_prompt, user_prompt).strip())
        task.effort_hours = effort_hours
        db.session.commit()
        return jsonify(TaskIASchema.from_orm(task).dict())
    except Exception as e:
        return jsonify({"error": f"Error al estimar esfuerzo: {str(e)}"}), 500

@ia_bp.route("/ai/tasks/audit", methods=["POST"])
def audit_task():
    data = request.json
    if not data.get("task_id"):
        return jsonify({"error": "task_id is required"}), 400
    task = Task.query.get(data["task_id"])
    if not task:
        return jsonify({"error": "Task not found"}), 404
    system_prompt = "Eres un experto en auditoría de riesgos de tareas de desarrollo de software. Tu tarea es analizar los posibles riesgos de la tarea y proponer un plan de mitigación. Devuelve el análisis y el plan en texto claro, que sea muy muy conciso."
    user_prompt = f"Audita la siguiente tarea:\nTítulo: {task.title}\n"
    if task.description:
        user_prompt += f"Descripción: {task.description}\n"
    risk_analysis = get_llm_response(system_prompt, user_prompt)
    return jsonify({"risk_analysis": risk_analysis, **TaskIASchema.from_orm(task).dict()}) 