# gui.py
from flask import Flask, render_template_string, request, redirect
import pandas as pd
import json, os, threading
from run import main_automation_process

app = Flask(__name__)
CONFIG_FILE = 'config.json'
LOG_FILE = 'application_log.csv'

@app.route('/', methods=['GET', 'POST'])
def index():
    conf = json.load(open(CONFIG_FILE, 'r'))
    if request.method == 'POST':
        form_filters = {
            "keywords": request.form['keywords'].split(','),
            "location": request.form['location'],
            "experience_level": request.form['experience_level']
        }
        conf['filters'] = form_filters
        conf['resume_path'] = request.form['resume_path']
        with open(CONFIG_FILE, 'w') as f:
            json.dump(conf, f)
        return redirect('/')
    df = pd.read_csv(LOG_FILE) if os.path.exists(LOG_FILE) else pd.DataFrame()
    return '<h2>Job Auto Applier - Edit config.json and run.py manually</h2>'

if __name__ == '__main__':
    app.run(port=8080, debug=True)
