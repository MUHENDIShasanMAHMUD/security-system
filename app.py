import sqlite3
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO

app = Flask(__name__, static_folder='.', template_folder='.')
socketio = SocketIO(app, cors_allowed_origins="*")
DATABASE = 'security_system.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute('CREATE TABLE IF NOT EXISTS sensor_events (id INTEGER PRIMARY KEY, distance REAL, timestamp TEXT, alarm_status BOOLEAN)')
    conn.commit()
    conn.close()

import urllib.request
from urllib.parse import quote

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/sensor/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    conn = sqlite3.connect(DATABASE)
    
    # إدخال البيانات في قاعدة البيانات
    conn.execute('INSERT INTO sensor_events (distance, timestamp, alarm_status) VALUES (?, ?, ?)', 
                 (data['distance'], data['timestamp'], data['alarm']))
    conn.commit()
    conn.close()
    
    # تحديث واجهة المستخدم عبر السوكت
    socketio.emit('sensor_update', data)
    

if __name__ == '__main__':
    init_db()
    socketio.run(app, host='0.0.0.0', port=5000)