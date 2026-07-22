from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

tasks = [
    {"id": 1, "title": "Learn Backend", "done": False},
    {"id": 2, "title": "Complete Data Structure Course", "done": False},
    {"id": 3, "title": "Get Healthier", "done": True}
]


@app.get("/")
def home():
    """
    Home Page
    ---
    responses:
      200:
        description: API info
    """
    return jsonify({"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}), 200


@app.get("/health")
def check():
    """
    Check Health
    ---
    responses:
      200:
        description: Health status
    """
    return jsonify({"status": "ok"}), 200


@app.get("/tasks")
def get_tasks():
    """
    Get all tasks
    ---
    responses:
      200:
        description: A list of tasks
    """
    return jsonify(tasks), 200


@app.get("/tasks/<int:id>")
def get_tasknum(id):
    """
    Get a task by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: The task
      404:
        description: Not found
    """
    for task in tasks:
        if task["id"] == id:
            return jsonify(task), 200
    return jsonify({'error': f"Task {id} Not found"}), 404


@app.post("/tasks")
def create_task():
    """
    Create a new task
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
    responses:
      201:
        description: Created
      400:
        description: Missing title
    """
    data = request.get_json(silent=True)

    if not data or "title" not in data or not data['title']:
        return jsonify({"error": "Task Title does not exist"}), 400

    new_task = {
        "id": tasks[-1]["id"] + 1 if tasks else 1,
        "title": data["title"],
        "done": False
    }

    tasks.append(new_task)
    return jsonify(new_task), 201


@app.put("/tasks/<int:id>")
def update_task(id):
    """
    Update a task
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
    responses:
      200:
        description: Updated task
      400:
        description: Empty/invalid body
      404:
        description: Task not found
    """
    data = request.get_json(silent=True)

    if not data or "title" not in data or not data["title"]:
        return jsonify({'error': 'Empty/Invalid Body'}), 400

    for task in tasks:
        if task["id"] == id:
            task["title"] = data["title"]
            return jsonify(task), 200

    return jsonify({'error': 'Unknown ID'}), 404


@app.delete('/tasks/<int:id>')
def delete_task(id):
    """
    Delete a task
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Task deleted
      404:
        description: Task not found
    """
    for task in tasks:
        if task['id'] == id:
            tasks.remove(task)
            return '', 204

    return jsonify({'error': 'Id not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)