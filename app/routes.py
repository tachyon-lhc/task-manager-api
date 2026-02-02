from flask import Blueprint, jsonify, request
from app.models import (
    create_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
    delete_task,
)

# Crear Blueprint (para organizar rutas)
api = Blueprint("api", __name__)


# Endpoints
@api.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = get_all_tasks()
    return jsonify(tasks), 200


@api.route("/tasks", methods=["POST"])
def create_task_endpoint():
    data = request.get_json()

    title = data.get("title")
    description = data.get("description", "")
    priority = data.get("priority", "medium")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    task_id = create_task(title, description, priority)

    new_task = get_task_by_id(task_id)

    return jsonify(new_task), 201


@api.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = get_task_by_id(task_id)
    if task:
        return jsonify(task), 200
    return jsonify({"error": "Task not found"}), 404


@api.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task_endpoint(task_id):
    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    completed = data.get("completed")
    priority = data.get("priority")

    success = update_task(task_id, title, description, completed, priority)

    if success:
        updated_task = get_task_by_id(task_id)
        return jsonify(updated_task), 200

    return jsonify({"error": "Task not found"}), 404


@api.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task_endpoint(task_id):
    result = delete_task(task_id)
    if result:
        return "", 204
    return jsonify({"error": "Task not found"}), 404
