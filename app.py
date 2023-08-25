from flask import Flask


app = Flask(__name__)

@app.route("/")
def init():
    return """<div style="width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; font-size: 32px;">Ivirse federated learning server</div>"""


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=False
    )