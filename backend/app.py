from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from pathlib import Path

from . import models, rewards

app = Flask(__name__, static_folder='../frontend')
CORS(app)

# initialize DB on startup
models.init_db()


@app.route('/api/letters', methods=['GET'])
def get_letters():
    letters = models.get_letters()
    # attach asset paths for letter pronunciation audio files
    # Audio files should be letter pronunciations (e.g., A.mp3 = "ay" sound)
    for l in letters:
        l['audio'] = f"/assets/audio/{l['letter']}.mp3"
    return jsonify({'letters': letters})


@app.route('/api/progress', methods=['POST'])
def post_progress():
    data = request.get_json() or {}
    letter = data.get('letter')
    correct = bool(data.get('correct', False))
    if not letter:
        return jsonify({'error': 'letter required'}), 400
    result = rewards.process_progress(letter.upper(), correct)
    return jsonify(result)


@app.route('/api/rewards', methods=['GET'])
def get_rewards():
    r = models.get_rewards()
    return jsonify(r)


@app.route('/api/init', methods=['POST'])
def api_init():
    models.init_db()
    return jsonify({'status': 'ok'})


# serve HTML pages
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'dashboard.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory(app.static_folder, 'dashboard.html')

@app.route('/login')
def login():
    return send_from_directory(app.static_folder, 'login.html')

# serve static files (CSS, JS, etc.) - only for specific file types to avoid catching API routes
import os

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(app.static_folder, 'css'), filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(app.static_folder, 'js'), filename)

# serve audio assets under /assets/audio/ (must come before general /assets/ route)
@app.route('/assets/audio/<path:filename>')
def assets_audio(filename):
    base = Path(__file__).resolve().parent.parent / 'frontend' / 'assets' / 'audio'
    return send_from_directory(base, filename)

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory(os.path.join(app.static_folder, 'assets'), filename)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
