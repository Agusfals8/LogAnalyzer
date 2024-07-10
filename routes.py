from flask import Flask, request, jsonify, Blueprint
from werkzeug.utils import secure_filename
import os
import dotenv
from log_analyzer import analyze_log

dotenv.load_dotenv()

app = Flask(__name__)
log_blueprint = Blueprint('log_blueprint', __name__)

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', './uploads')
ALLOWED_EXTENSIONS = set(['txt', 'log'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@log_blueprint.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400
        
@log_blueprint.route('/analyze/<filename>', methods=['GET'])
def analyze(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.isfile(filepath):
        result = analyze_log(filepath)
        return jsonify(result), 200
    else:
        return jsonify({'error': 'File not found'}), 404

@log_blueprint.route('/report/<filename>', methods=['GET'])
def get_report(filename):
    report_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.report")
    if os.path.isfile(report_path):
        with open(report_path, 'r') as report_file:
            content = report_file.read()
        return content
    else:
        return jsonify({'error': 'Report not found'}), 404

app.register_blueprint(log_blueprint, url_prefix='/logs')

if __name__ == '__main__':
    app.run(debug=True)