from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def home():
    return jsonify({"name":"Task API", "version": "1.0", "endpoints": ["/tasks"]}),200

@app.get("/health")
def check():
    return jsonify({"status":"ok"}), 200

if __name__ == '__main__':
    app.run(debug=True)