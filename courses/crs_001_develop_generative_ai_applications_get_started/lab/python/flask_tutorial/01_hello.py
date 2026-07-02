"""Flask bite 1 — Hello route.

Run:
    python 01_hello.py

Open: http://127.0.0.1:5000/
Stop: Ctrl+C
"""

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello from Flask — bite 1"


if __name__ == "__main__":
    app.run(debug=True)