"""
تعديلات على app.py لدمج نظام الإشعارات
أضف هذا الكود إلى app.py الأساسي
"""

# ==================== في أعلى الملف ====================
# من app.py الحالي
from notifications import send_all_notifications, get_notification_status, create_push_notification_payload

# ==================== أضف هذه المسارات الجديدة ====================

@app.route('/api/notifications/status', methods=['GET'])
def get_notifications_status():
    """الحصول على حالة نظام الإشعارات"""
    return jsonify(get_notification_status()), 200

@app.route('/api/notifications/test', methods=['POST'])
def test_notifications():
    """اختبار الإشعارات (للتطوير والاختبار)"""
    try:
        data = request.get_json()
        distance = data.get('distance', 15.5)
        timestamp = data.get('timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        alarm = data.get('alarm', True)
        
        results = send_all_notifications(distance, timestamp, alarm)
        
        return jsonify({
            'status': 'success',
            'message': 'Test notifications sent',
            'results': results
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notifications/configure', methods=['POST'])
def configure_notifications():
    """تكوين الإشعارات"""
    try:
        config = request.get_json()
        
        # تحديث إعدادات Telegram
        if 'telegram' in config:
            TELEGRAM_CONFIG['enabled'] = config['telegram'].get('enabled', False)
            TELEGRAM_CONFIG['bot_token'] = config['telegram'].get('bot_token', '')
            TELEGRAM_CONFIG['chat_id'] = config['telegram'].get('chat_id', '')
        
        # تحديث إعدادات البريد الإلكتروني
        if 'email' in config:
            EMAIL_CONFIG['enabled'] = config['email'].get('enabled', False)
            EMAIL_CONFIG['sender_email'] = config['email'].get('sender_email', '')
            EMAIL_CONFIG['sender_password'] = config['email'].get('sender_password', '')
            EMAIL_CONFIG['recipient_emails'] = config['email'].get('recipient_emails', [])
        
        # تحديث إعدادات Firebase
        if 'firebase' in config:
            FIREBASE_CONFIG['enabled'] = config['firebase'].get('enabled', False)
        
        return jsonify({
            'status': 'success',
            'message': 'Notifications configured',
            'config': get_notification_status()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== تعديل دالة استقبال البيانات ====================

@app.route('/api/sensor/data', methods=['POST'])
def receive_sensor_data():
    """
    Receive sensor data from Raspberry Pi Pico W
    Modified to include notifications
    """
    try:
        data = request.get_json()
        
        if not data or 'distance' not in data or 'timestamp' not in data:
            return jsonify({'error': 'Invalid data format'}), 400
        
        distance = float(data.get('distance'))
        timestamp = data.get('timestamp')
        alarm_status = data.get('alarm', False)
        
        # Insert into database
        if insert_sensor_data(distance, timestamp, alarm_status):
            print(f"📥 Data received: {distance}cm, Alarm: {alarm_status}")
            
            # Broadcast to WebSocket clients
            socketio.emit('sensor_update', {
                'distance': distance,
                'timestamp': timestamp,
                'alarm': alarm_status,
                'received_at': datetime.now().isoformat()
            }, broadcast=True)
            
            # If alarm triggered, send notifications
            if alarm_status:
                # إرسال الإشعارات
                send_all_notifications(distance, timestamp, alarm=True)
                
                # إرسال تنبيه WebSocket
                socketio.emit('alarm_alert', {
                    'distance': distance,
                    'timestamp': timestamp,
                    'message': '🚨 Motion detected!',
                    'notification': create_push_notification_payload(distance, timestamp, True)
                }, broadcast=True)
            
            return jsonify({
                'status': 'success',
                'message': 'Data stored successfully'
            }), 201
        else:
            return jsonify({'error': 'Database error'}), 500
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)}), 400

# ==================== مثال على استخدام الإشعارات ====================

"""
1. لتفعيل Telegram:
   POST /api/notifications/configure
   {
       "telegram": {
           "enabled": true,
           "bot_token": "YOUR_BOT_TOKEN",
           "chat_id": "YOUR_CHAT_ID"
       }
   }

2. لتفعيل البريد الإلكتروني:
   POST /api/notifications/configure
   {
       "email": {
           "enabled": true,
           "sender_email": "your@gmail.com",
           "sender_password": "app_password",
           "recipient_emails": ["recipient@gmail.com"]
       }
   }

3. لاختبار الإشعارات:
   POST /api/notifications/test
   {
       "distance": 15.5,
       "timestamp": "2026-01-15 14:30:45",
       "alarm": true
   }

4. للتحقق من حالة الإشعارات:
   GET /api/notifications/status
"""
