from flask import Flask, jsonify, render_template, request


def create_app():
    app = Flask(__name__)
    app.todos = [
        {"id": 1, "title": "Buy milk", "completed": False},
        {"id": 2, "title": "Walk the dog", "completed": False},
    ]

    def find_todo(todo_id):
        return next((t for t in app.todos if t["id"] == todo_id), None)

    @app.route("/")
    def index():
        return render_template("index.html", todos=app.todos)

    @app.route("/todos/<int:todo_id>", methods=["PATCH"])
    def update_todo(todo_id):
        todo = find_todo(todo_id)
        if todo is None:
            return jsonify(error="not found"), 404
        data = request.get_json(silent=True) or {}
        if not isinstance(data.get("completed"), bool):
            return jsonify(error="'completed' must be a boolean"), 400
        todo["completed"] = data["completed"]
        return jsonify(todo)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
