"""
أمثلة اختبار API كاملة
استخدم Postman أو curl أو هذا الملف
"""

import requests
import json
from datetime import datetime

# المتغيرات
BASE_URL = "http://localhost:5000"
HEADERS = {"Content-Type": "application/json"}

# ==================== اختبارات الصحة والمعلومات ====================

def test_health():
    """اختبار صحة الخادم"""
    print("\n🏥 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Error: {e}")

# ==================== اختبارات البيانات ====================

def test_send_sensor_data(distance=15.5, alarm=True):
    """إرسال بيانات حساس"""
    print(f"\n📡 Sending Sensor Data (Distance: {distance}cm, Alarm: {alarm})...")
    
    payload = {
        "distance": distance,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "alarm": alarm
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/sensor/data",
            headers=HEADERS,
            json=payload
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_get_events(limit=10):
    """جلب الأحداث الأخيرة"""
    print(f"\n📊 Fetching Recent Events (Limit: {limit})...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/events?limit={limit}")
        print(f"Status: {response.status_code}")
        events = response.json()
        print(f"Total Events: {len(events)}")
        if events:
            print(f"Latest Event: {json.dumps(events[0], indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_get_statistics():
    """جلب الإحصائيات"""
    print("\n📈 Fetching Statistics...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/statistics")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Error: {e}")

# ==================== اختبارات الإشعارات ====================

def test_notifications_status():
    """الحصول على حالة الإشعارات"""
    print("\n🔔 Fetching Notifications Status...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/notifications/status")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_send_test_notification(distance=15.5, alarm=True):
    """إرسال إشعار اختبار"""
    print(f"\n🧪 Sending Test Notification (Distance: {distance}cm, Alarm: {alarm})...")
    
    payload = {
        "distance": distance,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "alarm": alarm
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/notifications/test",
            headers=HEADERS,
            json=payload
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_configure_notifications():
    """تكوين الإشعارات"""
    print("\n⚙️  Configuring Notifications...")
    
    # مثال: تفعيل Telegram
    payload = {
        "telegram": {
            "enabled": False,  # غيّر إلى True لتفعيل
            "bot_token": "YOUR_TOKEN",
            "chat_id": "YOUR_CHAT_ID"
        },
        "email": {
            "enabled": False,
            "sender_email": "your@gmail.com",
            "sender_password": "app_password",
            "recipient_emails": ["recipient@gmail.com"]
        },
        "firebase": {
            "enabled": False
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/notifications/configure",
            headers=HEADERS,
            json=payload
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Error: {e}")

# ==================== اختبارات الإعدادات ====================

def test_get_settings():
    """جلب الإعدادات"""
    print("\n⚙️  Fetching Settings...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/settings")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_update_settings():
    """تحديث الإعدادات"""
    print("\n📝 Updating Settings...")
    
    payload = {
        "distance_threshold": 20,
        "update_interval_ms": 500,
        "timezone": "UTC",
        "notifications_enabled": True
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/settings",
            headers=HEADERS,
            json=payload
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Error: {e}")

# ==================== اختبارات التطهير ====================

def test_clear_data():
    """حذف جميع البيانات"""
    print("\n🗑️  Clearing All Data...")
    
    confirm = input("⚠️  Are you sure? This will delete all data! (yes/no): ")
    if confirm.lower() != 'yes':
        print("❌ Cancelled")
        return
    
    try:
        response = requests.delete(f"{BASE_URL}/api/clear-data")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Error: {e}")

# ==================== اختبار شامل ====================

def run_full_test():
    """تشغيل جميع الاختبارات"""
    print("=" * 60)
    print("🧪 FULL API TEST SUITE")
    print("=" * 60)
    
    # 1. اختبار الصحة
    test_health()
    
    # 2. إرسال بيانات اختبار
    print("\n" + "=" * 60)
    print("📤 Sending Test Data")
    print("=" * 60)
    
    test_send_sensor_data(distance=50.0, alarm=False)  # آمن
    test_send_sensor_data(distance=15.5, alarm=True)   # تنبيه
    test_send_sensor_data(distance=10.0, alarm=True)   # تنبيه
    
    # 3. جلب البيانات
    print("\n" + "=" * 60)
    print("📥 Retrieving Data")
    print("=" * 60)
    
    test_get_events(limit=5)
    test_get_statistics()
    
    # 4. اختبار الإشعارات
    print("\n" + "=" * 60)
    print("🔔 Notifications Test")
    print("=" * 60)
    
    test_notifications_status()
    # لا نرسل إشعار حقيقي إلا إذا كانت الإشعارات مفعلة
    
    # 5. الإعدادات
    print("\n" + "=" * 60)
    print("⚙️  Settings Test")
    print("=" * 60)
    
    test_get_settings()

# ==================== اختبار محاكاة البيكو ====================

def simulate_pico_readings():
    """محاكاة قراءات من البيكو"""
    print("\n🤖 Simulating Pico Readings...")
    
    import time
    
    # سيناريو 1: قراءات عادية
    readings = [
        (50.0, False),  # آمن
        (45.0, False),  # آمن
        (30.0, False),  # آمن
        (22.0, False),  # آمن
        (18.0, True),   # تنبيه!
        (15.5, True),   # تنبيه!
        (12.0, True),   # تنبيه!
        (25.0, False),  # ابتعاد
        (40.0, False),  # عودة
    ]
    
    for distance, alarm in readings:
        print(f"\n📍 Reading: {distance}cm, Alarm: {alarm}")
        test_send_sensor_data(distance=distance, alarm=alarm)
        time.sleep(1)  # انتظر ثانية بين القراءات

# ==================== القائمة الرئيسية ====================

def main():
    """القائمة الرئيسية"""
    
    print("\n" + "=" * 60)
    print("🔒 Smart Security System - API Test Suite")
    print("=" * 60)
    
    while True:
        print("\n📋 Options:")
        print("1. Health Check")
        print("2. Send Single Sensor Data")
        print("3. Get Recent Events")
        print("4. Get Statistics")
        print("5. Check Notifications Status")
        print("6. Send Test Notification")
        print("7. Configure Notifications")
        print("8. Get Settings")
        print("9. Update Settings")
        print("10. Simulate Pico Readings")
        print("11. Run Full Test")
        print("12. Clear All Data")
        print("0. Exit")
        
        choice = input("\n👉 Select option: ")
        
        try:
            if choice == '1':
                test_health()
            elif choice == '2':
                distance = float(input("Distance (cm): "))
                alarm = input("Alarm (true/false): ").lower() == 'true'
                test_send_sensor_data(distance, alarm)
            elif choice == '3':
                limit = int(input("Limit: "))
                test_get_events(limit)
            elif choice == '4':
                test_get_statistics()
            elif choice == '5':
                test_notifications_status()
            elif choice == '6':
                distance = float(input("Distance (cm): "))
                alarm = input("Alarm (true/false): ").lower() == 'true'
                test_send_test_notification(distance, alarm)
            elif choice == '7':
                test_configure_notifications()
            elif choice == '8':
                test_get_settings()
            elif choice == '9':
                test_update_settings()
            elif choice == '10':
                simulate_pico_readings()
            elif choice == '11':
                run_full_test()
            elif choice == '12':
                test_clear_data()
            elif choice == '0':
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid option")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
