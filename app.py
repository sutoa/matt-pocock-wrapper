from flask import Flask, jsonify, request


def create_app():
    app = Flask(__name__)
    app.todos = [
        {"id": 1, "title": "Buy milk", "completed": False},
        {"id": 2, "title": "Walk the dog", "completed": False},
    ]

    def find_todo(todo_id):
        return next((t for t in app.todos if t["id"] == todo_id), None)

    @app.route("/todos/<int:todo_id>", methods=["PATCH"])
    def update_todo(todo_id):
        todo = find_todo(todo_id)
        if todo is None:
            return jsonify(error="not found"), 404
        data = request.get_json(silent=True) or {}
        todo["completed"] = bool(data["completed"])
        return jsonify(todo)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
