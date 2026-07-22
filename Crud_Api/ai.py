from flask import Flask, jsonify, request
from flasgger import Swagger
from itertools import count

app = Flask(__name__)
app.config["SWAGGER"] = {
    "title": "Task API",
    "uiversion": 3,
}
swagger = Swagger(app)

# In-memory store. A dict keyed by id is used instead of a list so lookups,
# updates, and deletes are O(1) instead of O(n) linear scans.
tasks = {
    1: {"id": 1, "title": "Learn Backend", "done": False},
    2: {"id": 2, "title": "Complete Data Structure Course", "done": False},
    3: {"id": 3, "title": "Get Healthier", "done": True},
}

# A counter that always hands out the next id, so deleting tasks never
# causes id collisions or reuse (unlike tasks[-1]["id"] + 1).
_id_counter = count(start=len(tasks) + 1)


def next_id():
    return next(_id_counter)


def error(message, status):
    return jsonify({"error": message}), status


@app.errorhandler(404)
def not_found(e):
    """Catch-all so unknown routes return JSON instead of Flask's HTML 404 page."""
    return error("Resource not found", 404)


@app.errorhandler(405)
def method_not_allowed(e):
    return error("Method not allowed on this route", 405)


@app.get("/")
def home():
    """
    API info
    ---
    tags:
      - Meta
    responses:
      200:
        description: Basic info about the API and a link to the docs
    """
    return jsonify({
        "name": "Task API",
        "version": "1.0",
        "docs": "/apidocs",
        "endpoints": ["/tasks", "/tasks/<id>", "/health"],
    }), 200


@app.get("/health")
def health():
    """
    Health check
    ---
    tags:
      - Meta
    responses:
      200:
        description: Service is up
    """
    return jsonify({"status": "ok"}), 200


@app.get("/tasks")
def list_tasks():
    """
    List tasks
    ---
    tags:
      - Tasks
    parameters:
      - name: done
        in: query
        type: boolean
        required: false
        description: Filter by completion status (true/false)
    responses:
      200:
        description: A list of tasks, optionally filtered by `done`
    """
    done_param = request.args.get("done")
    values = list(tasks.values())

    if done_param is not None:
        wants_done = done_param.lower() == "true"
        values = [t for t in values if t["done"] == wants_done]

    return jsonify(values), 200


@app.get("/tasks/<int:task_id>")
def get_task(task_id):
    """
    Get a single task
    ---
    tags:
      - Tasks
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: The task
      404:
        description: No task with that id
    """
    task = tasks.get(task_id)
    if task is None:
        return error(f"Task {task_id} not found", 404)
    return jsonify(task), 200


@app.post("/tasks")
def create_task():
    """
    Create a task
    ---
    tags:
      - Tasks
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - title
          properties:
            title:
              type: string
            done:
              type: boolean
    responses:
      201:
        description: Task created
      400:
        description: Title missing, blank, or not a string
    """
    data = request.get_json(silent=True)

    if not data:
        return error("Request body must be JSON", 400)

    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        return error("Title is required and must be a non-empty string", 400)

    done = data.get("done", False)
    if not isinstance(done, bool):
        return error("'done' must be true or false", 400)

    task_id = next_id()
    task = {"id": task_id, "title": title.strip(), "done": done}
    tasks[task_id] = task

    return jsonify(task), 201


@app.put("/tasks/<int:task_id>")
def update_task(task_id):
    """
    Replace/update a task
    ---
    tags:
      - Tasks
    parameters:
      - name: task_id
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
            done:
              type: boolean
    responses:
      200:
        description: Updated task
      400:
        description: Invalid body
      404:
        description: No task with that id
    """
    task = tasks.get(task_id)
    if task is None:
        return error(f"Task {task_id} not found", 404)

    data = request.get_json(silent=True)
    if not data:
        return error("Request body must be JSON", 400)

    if "title" in data:
        title = data["title"]
        if not isinstance(title, str) or not title.strip():
            return error("Title must be a non-empty string", 400)
        task["title"] = title.strip()

    if "done" in data:
        done = data["done"]
        if not isinstance(done, bool):
            return error("'done' must be true or false", 400)
        task["done"] = done

    return jsonify(task), 200


@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    """
    Delete a task
    ---
    tags:
      - Tasks
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Task deleted
      404:
        description: No task with that id
    """
    if task_id not in tasks:
        return error(f"Task {task_id} not found", 404)

    del tasks[task_id]
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)