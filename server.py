from flask import Flask, render_template, jsonify, Response
from flask_cors import CORS
from subprocess import call
from flask_sse import sse

from config.file_dev import extra_watch
from config.sys_logging import get_lastest_logs
import psutil
import platform

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix="/stream")
fl_start = False
CORS(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/execute-fl-server",methods=["POST"])
def execute():
    global fl_start
    try:
        fl_start = True
        call(["python", "fl_server.py"])
        fl_start = False
        return jsonify({
            "code": 200,
            "message": "Success training task!"
        })
    except:
        return jsonify({
            "code": 500,
            "message": "Fail to training"
        })
        
@app.route("/logs")
# def get_logs():
#     def generate_logs():
#         lastestLogs = get_lastest_logs()
#         with open(lastestLogs, 'r') as f:
#             while True:
#                 line = f.readline()
#                 if not line:
#                     break
#                 yield f"data: {line}\n\n"
        
#     return Response(generate_logs(), mimetype="text/event-stream")
def get_logs():
    lastestLogs = get_lastest_logs()
    with open(lastestLogs, "r") as f:
        content = f.read()
        
    return jsonify({
        "code": 200,
        "message": content
    })
        
@app.route('/stats')
def get_server_stats():
    cpu_percent = psutil.cpu_percent()
    cpu_freq = psutil.cpu_freq().current
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    
    
    # Check platform system to get the system temperature
    system_temperatures = "---"
    if platform.system() != "Windows":
        system_temperatures = {}
        temps = psutil.sensors_temperatures()
        for name, entries in temps.items():
            for entry in entries:
                system_temperatures[entry.label] = entry.current


    # print(system_temperatures)
    stats = {
        'cpu_percent': cpu_percent,
        'cpu_freq': f"{(cpu_freq/1000):.2f}",
        'memory_percent': memory_percent,
        'disk_percent': disk_percent,
        'system_temperatures': system_temperatures
    }

    return jsonify(stats)
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True, extra_files=extra_watch())