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
    if request.is_json:
        request.data = request.get_json()

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)

db.create_all()

@app.route('/logs', methods=['POST'])
def add_log():
    content = request.data.get('content')
    if content:
        new_log = Log(content=content)
        db.session.add(new_log)
        db.search.commit()
        return jsonify({'message': 'Log added'}), 201
    else:
        return jsonify({'message': 'Content is required'}), 400

@app.route('/logs', methods=['GET'])
def get_logs():
    logs = Log.query.all()
    return jsonify([{'id': log.id, 'content': log.content} for log in logs]), 200

@app.route('/report', methods=['GET'])
def generate_report():
    return jsonify({'message': 'Report generated'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)