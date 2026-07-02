"""Flask bite 2 — JSON response + query param.

Run:
    python 02_json_route.py

Try:
    http://127.0.0.1:5000/
    http://127.0.0.1:5000/capital?country=Canada
"""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"message": "Flask bite 2 — try /capital?country=Canada"})


@app.route("/capital")
def capital():
    country = request.args.get("country", "")
    if not country:
        return jsonify({"error": "Add ?country=Canada"}), 400
    # Fake lookup — real lab will call an LLM here
    answers = {"Canada": "Ottawa", "France": "Paris"}
    city = answers.get(country)
    if not city:
        return jsonify({"error": f"No data for {country}"}), 404
    return jsonify({"country": country, "capital": city})


if __name__ == "__main__":
    app.run(debug=True)