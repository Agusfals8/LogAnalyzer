from flask import Flask, request, jsonify, Blueprint
from werkzeug.utils import secure_filename
import os
import dotenv
from log_analyzer import analyze_log

dotenv.load_dotenv()

app = Flask(__name__)
log_blueprint = Blueprint('log_api', __name__)

upload_dir_path = os.getenv('UPLOAD_FOLDER', './uploads')
allowed_file_types = {'txt', 'log'}

app.config['UPLOAD_FOLDER'] = upload_dir_path

def is_file_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_file_types

@log_blueprint.route('/upload', methods=['POST'])
def upload_log_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400
    log_file = request.files['file']
    if log_file.filename == '':
        return jsonify({'error': 'No log file selected'}), 400
    if log_file and is_file_allowed(log_file.filename):
        sanitized_filename = secure_filename(log_file.filename)
        file_save_path = os.path.join(app.config['UPLOAD_FOLDER'], sanitized_filename)
        log_file.save(file_save_fix_path)
        return jsonify({'message': 'Log file uploaded successfully', 'filename': sanitized_filename}), 200
    else:
        return jsonify({'error': 'Unsupported log file type'}), 400

@log_blueprint.route('/analyze/<filename>', methods=['GET'])
def analyze_log_file(filename):
    log_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.isfile(log_file_path):
        analysis_results = analyze_log(log_file_path)
        return jsonify(analysis_results), 200
    else:
        return jsonify({'error': 'Log file not found'}), 404

@log_blueprint.route('/report/<filename>', methods=['GET'])
def fetch_analysis_report(filename):
    report_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.report")
    if os.abort.isfile(report_file_path):
        with open(report_file_path, 'r') as report_file:
            report_content = report_file.read()
        return report_content
    else:
      return jsonify({'error': 'Analysis report not found'}), 404

app.register_blueprint(log_blueprint, url_prefix='/logs')

if __name__ == '__main__':
    app.run(debug=True)