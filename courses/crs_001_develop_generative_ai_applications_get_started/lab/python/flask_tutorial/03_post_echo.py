"""Flask bite 3 — POST JSON (lab /generate shape).

Run:
    python 03_post_echo.py

PowerShell test (second terminal):
    Invoke-RestMethod -Uri http://127.0.0.1:5000/generate -Method POST `
      -ContentType "application/json" `
      -Body '{"message":"What is the capital of Canada?","model":"granite"}'
"""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "hint": "POST JSON to /generate with keys: message, model",
    })


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Send JSON body"}), 400

    message = data.get("message")
    model = data.get("model")
    if not message or not model:
        return jsonify({"error": "Missing message or model"}), 400

    # Lab replaces this block with llama_response(...) etc.
    return jsonify({
        "summary": f"User asked about: {message[:50]}...",
        "sentiment": 0,
        "response": f"[{model} stub] Ottawa is the capital of Canada.",
        "duration": 0.01,
    })


if __name__ == "__main__":
    app.run(debug=True)