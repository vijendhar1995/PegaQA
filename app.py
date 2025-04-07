
from flask import Flask, render_template, request, jsonify
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    question = request.form['question']
    answer = request.form['answer']
    file = request.files.get('attachment')

    filename = None
    if file and file.filename:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        filename = filepath

    entry = {
        'question': question,
        'answer': answer,
        'attachment': filename,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    data = load_data()
    data.append(entry)
    save_data(data)
    return jsonify({'success': True})

@app.route('/data')
def get_data():
    return jsonify(load_data())

if __name__ == '__main__':
    app.run(debug=True, port=1432)
