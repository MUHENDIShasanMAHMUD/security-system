# Configuration File for Smart Security System
# قائمة الإعدادات المركزية للنظام

import json
import os
from datetime import datetime

# ==================== System Configuration ====================

class Config:
    """الإعدادات المركزية للنظام"""
    
    # Database
    DATABASE_PATH = 'security_system.db'
    DATABASE_BACKUP_PATH = 'backups/'
    AUTO_BACKUP_INTERVAL = 3600  # ثانية (كل ساعة)
    
    # Flask Server
    FLASK_HOST = '0.0.0.0'
    FLASK_PORT = 5000
    FLASK_DEBUG = False
    FLASK_ENV = 'development'  # أو 'production'
    
    # Wi-Fi Settings (للبيكو)
    WIFI_SSID = 'YOUR_NETWORK_NAME'
    WIFI_PASSWORD = 'YOUR_PASSWORD'
    WIFI_TIMEOUT = 10000  # ميلي ثانية
    
    # Server Communication
    SERVER_IP = '192.168.1.100'  # غيّره حسب جهازك
    SERVER_PORT = 5000
    SERVER_TIMEOUT = 5000  # ميلي ثانية
    
    # Sensor Settings
    DISTANCE_THRESHOLD = 20  # سم
    SENSOR_READ_INTERVAL = 500  # ميلي ثانية
    MAX_DISTANCE = 400  # سم
    
    # GPIO Pins (Pico)
    GPIO_TRIG = 15
    GPIO_ECHO = 14
    GPIO_LED_RED = 0
    GPIO_LED_GREEN = 1
    GPIO_BUZZER = 18
    
    # Alarm Settings
    ALARM_BEEPS = 3  # عدد النبضات
    ALARM_BEEP_DURATION = 100  # ميلي ثانية
    ALARM_AUTO_RESET = 60  # ثانية (0 = لا يُعاد)
    
    # NTP Settings
    NTP_SERVER = 'pool.ntp.org'
    NTP_TIMEOUT = 5000
    
    # Notifications (see notifications.py)
    NOTIFICATIONS_ENABLED = True
    NOTIFICATION_CHANNELS = ['browser_push']  # أضف 'telegram', 'email' حسب الحاجة
    
    # Logging
    LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR
    LOG_FILE = 'security_system.log'
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
    
    # API Settings
    API_RATE_LIMIT = '100 per hour'
    API_CORS_ORIGINS = ['*']
    
    # Frontend
    FRONTEND_REFRESH_INTERVAL = 5000  # ميلي ثانية
    FRONTEND_TABLE_ROWS = 50
    
    # Security
    API_SECRET_KEY = 'change-this-to-a-random-secret-key'
    REQUIRE_AUTHENTICATION = False
    
    @classmethod
    def to_dict(cls):
        """تحويل الإعدادات إلى قاموس"""
        return {
            'database': {
                'path': cls.DATABASE_PATH,
                'backup_path': cls.DATABASE_BACKUP_PATH,
                'auto_backup_interval': cls.AUTO_BACKUP_INTERVAL
            },
            'flask': {
                'host': cls.FLASK_HOST,
                'port': cls.FLASK_PORT,
                'debug': cls.FLASK_DEBUG,
                'env': cls.FLASK_ENV
            },
            'wifi': {
                'ssid': cls.WIFI_SSID,
                'password': '***hidden***',  # لا نعرض كلمة المرور
                'timeout': cls.WIFI_TIMEOUT
            },
            'server': {
                'ip': cls.SERVER_IP,
                'port': cls.SERVER_PORT,
                'timeout': cls.SERVER_TIMEOUT
            },
            'sensor': {
                'distance_threshold': cls.DISTANCE_THRESHOLD,
                'read_interval': cls.SENSOR_READ_INTERVAL,
                'max_distance': cls.MAX_DISTANCE
            },
            'gpio': {
                'trig': cls.GPIO_TRIG,
                'echo': cls.GPIO_ECHO,
                'led_red': cls.GPIO_LED_RED,
                'led_green': cls.GPIO_LED_GREEN,
                'buzzer': cls.GPIO_BUZZER
            },
            'alarm': {
                'beeps': cls.ALARM_BEEPS,
                'beep_duration': cls.ALARM_BEEP_DURATION,
                'auto_reset': cls.ALARM_AUTO_RESET
            },
            'notifications': {
                'enabled': cls.NOTIFICATIONS_ENABLED,
                'channels': cls.NOTIFICATION_CHANNELS
            }
        }
    
    @classmethod
    def save_to_file(cls, filename='config.json'):
        """حفظ الإعدادات في ملف JSON"""
        config_dict = cls.to_dict()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2, ensure_ascii=False)
        print(f"✓ Config saved to {filename}")
    
    @classmethod
    def load_from_file(cls, filename='config.json'):
        """تحميل الإعدادات من ملف JSON"""
        if not os.path.exists(filename):
            print(f"⚠️  Config file not found: {filename}")
            return False
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                config_dict = json.load(f)
            
            # تحديث الإعدادات
            for key, value in config_dict.items():
                if key == 'database':
                    cls.DATABASE_PATH = value.get('path', cls.DATABASE_PATH)
                    cls.AUTO_BACKUP_INTERVAL = value.get('auto_backup_interval', cls.AUTO_BACKUP_INTERVAL)
                elif key == 'flask':
                    cls.FLASK_HOST = value.get('host', cls.FLASK_HOST)
                    cls.FLASK_PORT = value.get('port', cls.FLASK_PORT)
                    cls.FLASK_DEBUG = value.get('debug', cls.FLASK_DEBUG)
                elif key == 'wifi':
                    cls.WIFI_SSID = value.get('ssid', cls.WIFI_SSID)
                    cls.WIFI_PASSWORD = value.get('password', cls.WIFI_PASSWORD)
                elif key == 'server':
                    cls.SERVER_IP = value.get('ip', cls.SERVER_IP)
                    cls.SERVER_PORT = value.get('port', cls.SERVER_PORT)
                elif key == 'sensor':
                    cls.DISTANCE_THRESHOLD = value.get('distance_threshold', cls.DISTANCE_THRESHOLD)
                    cls.SENSOR_READ_INTERVAL = value.get('read_interval', cls.SENSOR_READ_INTERVAL)
                elif key == 'alarm':
                    cls.ALARM_BEEPS = value.get('beeps', cls.ALARM_BEEPS)
                    cls.ALARM_AUTO_RESET = value.get('auto_reset', cls.ALARM_AUTO_RESET)
                elif key == 'notifications':
                    cls.NOTIFICATIONS_ENABLED = value.get('enabled', cls.NOTIFICATIONS_ENABLED)
                    cls.NOTIFICATION_CHANNELS = value.get('channels', cls.NOTIFICATION_CHANNELS)
            
            print(f"✓ Config loaded from {filename}")
            return True
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return False

# ==================== استخدام ====================

if __name__ == '__main__':
    # اطبع الإعدادات الحالية
    print("📋 Current Configuration:")
    print(json.dumps(Config.to_dict(), indent=2, ensure_ascii=False))
    
    # احفظ الإعدادات في ملف
    print("\n💾 Saving configuration...")
    Config.save_to_file('config.json')
    
    # اختبر التحميل
    print("\n📂 Loading configuration...")
    Config.load_from_file('config.json')
    
    # اطبع الإعدادات بعد التحميل
    print("\n✓ Configuration ready!")
    print(f"Flask will run on: {Config.FLASK_HOST}:{Config.FLASK_PORT}")
    print(f"Database: {Config.DATABASE_PATH}")
    print(f"Distance Threshold: {Config.DISTANCE_THRESHOLD} cm")
