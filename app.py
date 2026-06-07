import sqlite3
from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO

app = Flask(__name__, static_folder='.', template_folder='.')
socketio = SocketIO(app, cors_allowed_origins="*")
DATABASE = 'security_system.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute('CREATE TABLE IF NOT EXISTS sensor_events (id INTEGER PRIMARY KEY, distance REAL, timestamp TEXT, alarm_status BOOLEAN)')
    conn.commit(); conn.close()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/sensor/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    conn = sqlite3.connect(DATABASE)
    conn.execute('INSERT INTO sensor_events (distance, timestamp, alarm_status) VALUES (?, ?, ?)', 
                 (data['distance'], data['timestamp'], data['alarm']))
    conn.commit(); conn.close()
    socketio.emit('sensor_update', data)
    return jsonify({'status': 'success'}), 201
import requests # تحتاج لتثبيت هذه المكتبة: pip install requests

def send_telegram_alert(message):
    token = "توكن_البوت_الخاص_بك"
    chat_id = "الـ_ID_الخاص_بك"
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url)

# داخل دالة receive_data في app.py
@app.route('/api/sensor/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    if data['alarm']: # إذا كان هناك إنذار
        send_telegram_alert(f"🚨 تنبيه: تم اكتشاف حركة! المسافة: {data['distance']} سم")
    # ... بقية الكود

if __name__ == '__main__':
    init_db()
    socketio.run(app, host='0.0.0.0', port=5000)