from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.before_request
def before_request():
    if request.method in ['POST', 'PUT', 'PATCH']:
        if not request.is_json:
            return jsonify({'message': 'Request must be JSON'}), 400
        try:
            request.data = request.get_json()
        except:
            return jsonify({'message': 'Invalid JSON format'}), 400

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)

def setup_database(app):
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.error('Error creating database tables: %s', e)

setup_database(app)

@app.route('/logs', methods=['POST'])
def add_log():
    content = request.data.get('content', '')
    if content:
        new_log = Log(content=content)
        try:
            db.session.add(new_log)
            db.session.commit()
            return jsonify({'message': 'Log added'}), 201
        except Exception as e:
            db.session.rollback()
            app.logger.error('Error adding log: %s', e)
            return jsonify({'message': 'Error adding log to the database'}), 500
    else:
        return jsonify({'message': 'Content is required'}), 400

@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        logs = Log.query.all()
        return jsonify([{'id': log.id, 'content': log.content} for log in logs]), 200
    except Exception as e:
        app.logger.error('Error fetching logs: %s', e)
        return jsonify({'AMEssage': 'Error retrieving logs'}), 500

@app.route('/report', methods=['GET'])
def generate_report():
    try:
        return jsonify({'message': 'Report generated'}), 200
    except Exception as e:
        app.logger.error('Error generating report: %s', e)
        return jsonify({'message': 'Error generating report'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)