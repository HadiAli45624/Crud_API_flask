from flask import Flask, jsonify

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



if __name__ == '__main__':
    app.run(debug=True)