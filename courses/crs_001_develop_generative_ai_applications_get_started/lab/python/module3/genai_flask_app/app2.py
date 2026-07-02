"""Lab Flask app (copy of app.py) — POST /generate + render_template on /.

Run:
    python app2.py
"""

import time

from flask import Flask, jsonify, render_template, request

from model import granite_response, llama_response, mistral_response

app = Flask(__name__)

SYSTEM_PROMPT = "You are an AI assistant helping with customer inquiries."

MODEL_HANDLERS = {
    "llama": llama_response,
    "granite": granite_response,
    "mistral": mistral_response,
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Send JSON body"}), 400

    user_message = data.get("message")
    model_name = data.get("model")

    if not user_message or not model_name:
        return jsonify({"error": "Missing message or model selection"}), 400

    handler = MODEL_HANDLERS.get(model_name)
    if handler is None:
        return jsonify({"error": "Invalid model selection"}), 400

    start_time = time.time()
    try:
        result = handler(SYSTEM_PROMPT, user_message)
        result["duration"] = round(time.time() - start_time, 3)
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(debug=True)