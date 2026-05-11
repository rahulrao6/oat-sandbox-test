"""Flask API backend for the calculator web UI."""

from flask import Flask, render_template, request, jsonify
from calculator import add, subtract, multiply, divide

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request: no JSON body"}), 400

    a = data.get("a")
    b = data.get("b")
    operation = data.get("operation")

    if a is None or b is None:
        return jsonify({"error": "Missing operands 'a' and/or 'b'"}), 400
    if operation is None:
        return jsonify({"error": "Missing 'operation' field"}), 400

    try:
        a = float(a)
        b = float(b)
    except (TypeError, ValueError):
        return jsonify({"error": "Operands must be numbers"}), 400

    ops = {
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide,
    }

    if operation not in ops:
        return jsonify({"error": f"Unknown operation '{operation}'. Use: add, subtract, multiply, divide"}), 400

    try:
        result = ops[operation](a, b)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)
