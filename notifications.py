"""
نظام الإشعارات المتقدم للتطبيق
يدعم: Telegram, Email, Browser Push, Firebase
"""

import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import json

# ==================== إعدادات الإشعارات ====================

# Telegram Configuration
TELEGRAM_CONFIG = {
    'enabled': False,
    'bot_token': 'YOUR_TELEGRAM_BOT_TOKEN',
    'chat_id': 'YOUR_CHAT_ID'
}

# Email Configuration
EMAIL_CONFIG = {
    'enabled': False,
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your_email@gmail.com',
    'sender_password': 'your_app_password',  # استخدم App Password من Google
    'recipient_emails': ['recipient@gmail.com']
}

# Browser Push Configuration (مع Service Worker)
BROWSER_PUSH_CONFIG = {
    'enabled': True,  # تُرسل عبر WebSocket
    'vapid_public_key': 'YOUR_VAPID_PUBLIC_KEY',
    'vapid_private_key': 'YOUR_VAPID_PRIVATE_KEY'
}

# Firebase Configuration
FIREBASE_CONFIG = {
    'enabled': False,
    'credentials_path': 'firebase-credentials.json',
    'project_id': 'your-project-id'
}

# ==================== Telegram Notifications ====================

def send_telegram_notification(distance, timestamp, alarm=False):
    """
    إرسال إشعار عبر Telegram
    
    للحصول على Bot Token:
    1. تحدث مع BotFather على Telegram
    2. أنشئ bot جديد
    3. احصل على التوكن
    
    للحصول على Chat ID:
    1. أضف البوت إلى مجموعتك
    2. أرسل رسالة
    3. اذهب إلى: https://api.telegram.org/botYOUR_TOKEN/getUpdates
    4. ابحث عن "chat" في الرد
    """
    if not TELEGRAM_CONFIG['enabled']:
        return
    
    try:
        token = TELEGRAM_CONFIG['bot_token']
        chat_id = TELEGRAM_CONFIG['chat_id']
        
        if alarm:
            emoji = "🚨"
            title = "تنبيه حركة مكتشفة!"
            color = "⚠️"
        else:
            emoji = "✅"
            title = "نظام طبيعي"
            color = "✓"
        
        message = f"""
{emoji} *نظام الأمان الذكي*

{title}
━━━━━━━━━━━━━━━━━━
📏 المسافة: {distance:.2f} cm
⏰ الوقت: {timestamp}
{color} الحالة: {'تنبيه' if alarm else 'آمن'}
━━━━━━━━━━━━━━━━━━
"""
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, json=payload, timeout=5)
        
        if response.status_code == 200:
            print("✓ Telegram notification sent")
            return True
        else:
            print(f"❌ Telegram error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Telegram error: {e}")
        return False

# ==================== Email Notifications ====================

def send_email_notification(distance, timestamp, alarm=False):
    """
    إرسال إشعار عبر البريد الإلكتروني
    
    لتفعيل Gmail:
    1. فعّل 2-Step Verification على حسابك
    2. اذهب إلى: https://myaccount.google.com/apppasswords
    3. اختر "Mail" و "Windows Computer"
    4. استخدم الـ 16 حرف كلمة المرور
    """
    if not EMAIL_CONFIG['enabled']:
        return
    
    try:
        subject = f"{'🚨 تنبيه' if alarm else '✅ تحديث'} نظام الأمان - {distance:.2f} cm"
        
        html_content = f"""
        <html dir="rtl">
        <head>
            <style>
                body {{ font-family: Arial; direction: rtl; }}
                .alert {{ background: {'#ffcccc' if alarm else '#ccffcc'}; padding: 20px; border-radius: 10px; }}
                .header {{ color: {'red' if alarm else 'green'}; font-size: 24px; font-weight: bold; }}
                .info {{ margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="alert">
                <div class="header">{'🚨 تنبيه حركة' if alarm else '✅ نظام آمن'}</div>
                <div class="info">
                    <p><strong>المسافة:</strong> {distance:.2f} cm</p>
                    <p><strong>الوقت:</strong> {timestamp}</p>
                    <p><strong>الحالة:</strong> {'تنبيه نشط' if alarm else 'جميع الأنظمة عاملة'}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg = MIMEText(html_content, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = ', '.join(EMAIL_CONFIG['recipient_emails'])
        
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
            server.sendmail(
                EMAIL_CONFIG['sender_email'],
                EMAIL_CONFIG['recipient_emails'],
                msg.as_string()
            )
        
        print("✓ Email notification sent")
        return True
        
    except Exception as e:
        print(f"❌ Email error: {e}")
        return False

# ==================== Browser Push Notifications ====================

def create_push_notification_payload(distance, timestamp, alarm=False):
    """
    إنشاء حمولة إشعار متصفح
    يتم إرسالها عبر WebSocket إلى جميع العملاء المتصلين
    """
    payload = {
        'title': '🚨 نظام الأمان' if alarm else '✅ تحديث النظام',
        'body': f"المسافة: {distance:.2f} cm\n{timestamp}",
        'icon': 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">{"🚨" if alarm else "✅"}</text></svg>',
        'badge': 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" fill="%23{"ff0000" if alarm else "00cc00"}"/></svg>',
        'tag': 'security-alert' if alarm else 'security-update',
        'requireInteraction': alarm,  # اجعل المستخدم ينقر على الإشعار
        'data': {
            'distance': distance,
            'timestamp': timestamp,
            'alarm': alarm,
            'url': 'http://localhost:5000'
        }
    }
    return payload

# ==================== Firebase Cloud Messaging ====================

def send_firebase_notification(distance, timestamp, alarm=False):
    """
    إرسال إشعار عبر Firebase
    
    للإعداد:
    1. اذهب إلى Firebase Console
    2. أنشئ مشروع جديد
    3. حمّل Service Account Key (JSON)
    4. ضعها في مجلد المشروع باسم firebase-credentials.json
    """
    if not FIREBASE_CONFIG['enabled']:
        return
    
    try:
        import firebase_admin
        from firebase_admin import credentials, messaging
        
        # تهيئة Firebase (مرة واحدة فقط)
        if not firebase_admin._apps:
            cred = credentials.Certificate(FIREBASE_CONFIG['credentials_path'])
            firebase_admin.initialize_app(cred)
        
        message = messaging.Message(
            notification=messaging.Notification(
                title='🚨 تنبيه الحركة' if alarm else '✅ تحديث النظام',
                body=f"المسافة: {distance:.2f} cm | {timestamp}"
            ),
            webpush=messaging.WebpushConfig(
                data={
                    'distance': str(distance),
                    'timestamp': timestamp,
                    'alarm': str(alarm).lower(),
                    'click_action': 'http://localhost:5000'
                }
            ),
            topic='security_alerts'
        )
        
        response = messaging.send(message)
        print(f"✓ Firebase notification sent: {response}")
        return True
        
    except Exception as e:
        print(f"❌ Firebase error: {e}")
        return False

# ==================== إرسال موحد ====================

def send_all_notifications(distance, timestamp, alarm=False):
    """
    إرسال إشعار عبر جميع القنوات المفعلة
    """
    print(f"\n📢 Sending notifications (Distance: {distance:.2f}cm, Alarm: {alarm})")
    
    results = {
        'telegram': send_telegram_notification(distance, timestamp, alarm),
        'email': send_email_notification(distance, timestamp, alarm),
        'firebase': send_firebase_notification(distance, timestamp, alarm),
    }
    
    return results

def get_notification_status():
    """الحصول على حالة الإشعارات المفعلة"""
    return {
        'telegram': TELEGRAM_CONFIG['enabled'],
        'email': EMAIL_CONFIG['enabled'],
        'browser_push': BROWSER_PUSH_CONFIG['enabled'],
        'firebase': FIREBASE_CONFIG['enabled']
    }

# ==================== مثال على الاستخدام ====================

if __name__ == '__main__':
    # اختبر الإشعارات
    print("Testing Notification System...")
    
    # مثال 1: إشعار تنبيه
    print("\n1. Testing Alarm Notification:")
    results = send_all_notifications(
        distance=15.5,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        alarm=True
    )
    print(f"Results: {results}")
    
    # مثال 2: إشعار عادي
    print("\n2. Testing Normal Update:")
    results = send_all_notifications(
        distance=50.0,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        alarm=False
    )
    print(f"Results: {results}")
    
    # احصل على حالة الإشعارات
    print("\n3. Notification Status:")
    status = get_notification_status()
    print(json.dumps(status, indent=2))
