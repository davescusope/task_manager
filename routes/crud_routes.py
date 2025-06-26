from flask import Blueprint, request, jsonify
from task_manager.models import Task
from task_manager.models.db import db
from task_manager.models.schemas import TaskClassicSchema

crud_bp = Blueprint("crud", __name__)

@crud_bp.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    result = {"tasks": [TaskClassicSchema.from_orm(task).dict() for task in tasks]}
    return jsonify(result)

@crud_bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(TaskClassicSchema.from_orm(task).dict())

@crud_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    prioridad_valida = {'baja', 'media', 'alta', 'bloqueante'}
    status_valido = {'pendiente', 'en progreso', 'en revisión', 'completada'}
    if data["priority"].lower() not in prioridad_valida:
        return jsonify({"error": f"Valor de prioridad inválido: '{data['priority']}'. Debe ser uno de: baja, media, alta, bloqueante."}), 400
    if data["status"].lower() not in status_valido:
        return jsonify({"error": f"Valor de status inválido: '{data['status']}'. Debe ser uno de: pendiente, en progreso, en revisión, completada."}), 400
    task = Task(
        title=data["title"],
        description=data["description"],
        priority=data["priority"].lower(),
        effort_hours=data["effort_hours"],
        status=data["status"].lower(),
        assigned_to=data["assigned_to"],
        user_story_id=None
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(TaskClassicSchema.from_orm(task).dict()), 201

@crud_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    data = request.json
    if "title" in data:
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"]
    if "priority" in data:
        prioridad_valida = {'baja', 'media', 'alta', 'bloqueante'}
        if data["priority"].lower() not in prioridad_valida:
            return jsonify({"error": f"Valor de prioridad inválido: '{data['priority']}'. Debe ser uno de: baja, media, alta, bloqueante."}), 400
        task.priority = data["priority"].lower()
    if "effort_hours" in data:
        task.effort_hours = data["effort_hours"]
    if "status" in data:
        status_valido = {'pendiente', 'en progreso', 'en revisión', 'completada'}
        if data["status"].lower() not in status_valido:
            return jsonify({"error": f"Valor de status inválido: '{data['status']}'. Debe ser uno de: pendiente, en progreso, en revisión, completada."}), 400
        task.status = data["status"].lower()
    if "assigned_to" in data:
        task.assigned_to = data["assigned_to"]
    if "user_story_id" in data:
        task.user_story_id = data["user_story_id"]
    db.session.commit()
    return jsonify(TaskClassicSchema.from_orm(task).dict())

@crud_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}) 