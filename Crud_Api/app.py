from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Learn Backend", "done": False},
    {"id": 2, "title": "Complete Data Structure Course", "done": False},
    {"id": 3, "title": "Get Healthier", "done": True}
]

@app.get("/")
def home():
    return jsonify({"name":"Task API", "version": "1.0", "endpoints": ["/tasks"]}),200

@app.get("/health")
def check():
    return jsonify({"status":"ok"}), 200

@app.get("/tasks")
def get_tasks():
    return jsonify(tasks), 200

@app.get("/tasks/<int:id>")
def get_tasknum(id):
    for task in tasks:
        if task["id"] == id:
            return jsonify(task),200
    return jsonify({'error': f"Task {id} Not found"}), 404

@app.post("/tasks")
def create_task():
    data = request.get_json()

    if "title" not in data or not data['title']:
        return jsonify({"error": "Task Title does not exist"}), 400

    new_task = { "id" : tasks[-1]["id"] + 1, "title" : data["title"], "done": False}

    tasks.append(new_task)
    return jsonify(new_task), 201

@app.put("/tasks/<int:id>")
def update_task(id):
    data = request.get_json()

    if "title" not in data or not data["title"]:
        return jsonify({'error': 'Empty/Invalid Body'}), 400

    for task in tasks:
        if task["id"] == id:
            task["title"] = data["title"]
            return jsonify(task), 200
        
    return jsonify({'error': 'Unknown ID'}), 404


@app.delete('/tasks/<int:id>')
def delete_task(id):
    for task in tasks:
        if task['id'] == id:
            tasks.remove(task)
            return jsonify({"No Content": ""}), 204

    return jsonify({'error': 'Id not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)