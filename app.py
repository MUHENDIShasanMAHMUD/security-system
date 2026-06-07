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

def send_telegram_alert(message):
    token = "8828447054:AAEBhzOFYXtn1IT83BDpz4LtZnAQwbhmzBs"
    chat_id = "7367505782"
    
    from urllib.parse import quote
    msg_encoded = quote(message)
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg_encoded}"
    
    # تعريف بروكسي عام لتجاوز حظر الـ DNS
    proxies = {
        'http': 'http://51.158.117.88:8811',
        'https': 'http://51.158.117.88:8811'
    }
    
    try:
        # إضافة proxies و timeout
        response = requests.get(url, proxies=proxies, timeout=10)
        if response.status_code == 200:
            print("Telegram Alert Sent via Proxy!")
        else:
            print(f"Telegram Failed, Status: {response.status_code}")
    except Exception as e:
        print("Telegram Alert Error:", e)
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
    
    # إرسال تنبيه تليجرام إذا كان هناك خطر حقيقي (alarm == True)
    if data.get('alarm'):
        alert_msg = f"🚨 تنبيه أمني! تم اكتشاف جسم على مسافة: {data['distance']} سم"
        send_telegram_alert(alert_msg)
        
    return jsonify({'status': 'success'}), 201

if __name__ == '__main__':
    init_db()
    socketio.run(app, host='0.0.0.0', port=5000)