from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Set up CI pipeline", "status": "done", "priority": "high", "created_at": "2026-05-01"},
    {"id": 2, "title": "Write unit tests", "status": "in_progress", "priority": "medium", "created_at": "2026-05-10"},
    {"id": 3, "title": "Deploy to staging", "status": "pending", "priority": "high", "created_at": "2026-05-15"},
]
next_id = 4

def find_task(task_id):
    return next((t for t in tasks if t["id"] == task_id), None)

def validate_task(data, require_all=True):
    errors = []
    if require_all and "title" not in data:
        errors.append("title is required")
    if "title" in data and not isinstance(data["title"], str):
        errors.append("title must be a string")
    if "status" in data and data["status"] not in ("pending", "in_progress", "done"):
        errors.append("status must be pending, in_progress, or done")
    if "priority" in data and data["priority"] not in ("low", "medium", "high"):
        errors.append("priority must be low, medium, or high")
    return errors

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "resource not found"}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "method not allowed"}), 405

@app.route("/tasks", methods=["GET"])
def get_tasks():
    status_filter = request.args.get("status")
    result = tasks
    if status_filter:
        if status_filter not in ("pending", "in_progress", "done"):
            return jsonify({"error": "invalid status filter"}), 400
        result = [t for t in tasks if t["status"] == status_filter]
    return jsonify({"tasks": result, "count": len(result)}), 200

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({"error": f"task {task_id} not found"}), 404
    return jsonify(task), 200

@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "request body must be JSON"}), 400
    errors = validate_task(data, require_all=True)
    if errors:
        return jsonify({"error": "validation failed", "details": errors}), 422
    task = {
        "id": next_id,
        "title": data["title"],
        "status": data.get("status", "pending"),
        "priority": data.get("priority", "medium"),
        "created_at": datetime.utcnow().strftime("%Y-%m-%d"),
    }
    tasks.append(task)
    next_id += 1
    return jsonify(task), 201

@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({"error": f"task {task_id} not found"}), 404
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "request body must be JSON"}), 400
    errors = validate_task(data, require_all=False)
    if errors:
        return jsonify({"error": "validation failed", "details": errors}), 422
    for field in ("title", "status", "priority"):
        if field in data:
            task[field] = data[field]
    return jsonify(task), 200

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({"error": f"task {task_id} not found"}), 404
    tasks.remove(task)
    return jsonify({"message": f"task {task_id} deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
