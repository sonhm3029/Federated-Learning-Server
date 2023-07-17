from flask import Flask, render_template, jsonify
from flask_cors import CORS
from subprocess import call

from config.file_dev import extra_watch

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/execute-fl-server",methods=["POST"])
def execute():
    try:
        call(["python", "fl_server.py"])
        return jsonify({
            "code": 200,
            "message": "Success training task!"
        })
    except:
        return jsonify({
            "code": 500,
            "message": "Fail to training"
        })

if __name__ == "__main__":
    # call(["python", "fl_server.py"])
    app.run(host="0.0.0.0", port=8000, debug=True, extra_files=extra_watch())
    print("OK")