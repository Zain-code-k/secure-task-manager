
from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = []
next_task_id = 1


@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Secure Task Manager!",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    global next_task_id

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "A non-empty title is required"}), 400

    if len(title.strip()) > 200:
        return jsonify({"error": "Title must be 200 characters or fewer"}), 400

    task = {
        "id": next_task_id,
        "title": title.strip(),
        "completed": False
    }

    tasks.append(task)
    next_task_id += 1

    return jsonify(task), 201


if __name__ == "__main__":
    app.run(debug=True)
