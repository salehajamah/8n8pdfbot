# دليل النشر - منشئ المحتوى الذكي

## خطوات النشر على Render.com

### 1. إعداد المستودع
```bash
# إنشاء مستودع Git جديد
git init
git add .
git commit -m "Initial commit: AI Content Creator Bot"

# رفع المشروع إلى GitHub
git remote add origin https://github.com/your-username/brochure-bot.git
git push -u origin main
```

## 3. النشر على Render

1.  **ربط Render بـ GitHub:**
    - اذهب إلى [render.com](https://render.com)
    - سجل الدخول باستخدام حساب GitHub الخاص بك.
    - اتبع التعليمات لربط المستودع الذي أنشأته للتو.

2.  **إعداد المتغيرات البيئية:**
    - في لوحة تحكم Render، انتقل إلى إعدادات خدمة `brochure-bot`.
    - أضف المتغيرات البيئية التالية:
        - `TELEGRAM_BOT_TOKEN`: توكن البوت الخاص بك من BotFather.
        - `OPENAI_API_KEY`: مفتاح API الخاص بك من OpenAI.
        - `WEB_APP_URL`: رابط تطبيقك الذي سيتم إنشاؤه على Render (مثال: `https://your-app.onrender.com`).
        - `TELEGRAM_PROVIDER_TOKEN`: توكن مزود الدفع الخاص بك من Telegram (إذا كنت تستخدم نظام الدفع).

3.  **تعيين أمر البناء:**
    - في قسم "Build Command"، أدخل الأمر التالي:
    ```bash
    pip install -r requirements.txt
    ```

4.  **تعيين أمر التشغيل:**
    - في قسم "Start Command"، أدخل الأمر التالي:
    ```bash
    python main.py
    ```

5.  **النشر:**
    - احفظ التغييرات. سيقوم Render بنشر التطبيق تلقائيًا.

## 4. إعداد البوت

1.  **إنشاء بوت تليجرام:**
    - تحدث مع `@BotFather` على تليجرام.
    - استخدم الأمر `/newbot`.
    - احفظ الـ Token المُعطى.

2.  **إعداد WebApp:**
    - استخدم الأمر `/newapp` مع `@BotFather`.
    - اربط WebApp بالبوت.
    - حدد URL التطبيق: `https://your-app-name.onrender.com`

3.  **إعداد Webhook:**
    - بعد النشر، قم بتعيين webhook للبوت باستخدام الرابط الذي حصلت عليه من Render:
    ```bash
    curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_APP_URL>/telegram-webhook"
    ```
    مثال:
    ```
    https://api.telegram.org/bot8302021134:AAH9660xbvFdAv-CCgLr_FdX_DPU2EgpawI/setWebhook?url=https://brochure-bot.onrender.com/telegram-webhook
    ```
    يجب أن تحصل على استجابة `{"ok":true,"result":true,"description":"Webhook was set"}`.

## 5. اختبار البوت

1.  افتح تليجرام وابحث عن البوت الخاص بك.
2.  أرسل الأمر `/start`.
3.  يجب أن يظهر لك زر "🚀 ابدأ مشروعًا جديدًا". اضغط عليه لفتح WebApp.
4.  املأ النموذج واختبر إنشاء المحتوى.

إذا واجهت أي مشاكل في أي خطوة، فلا تتردد في إخباري. أنا هنا للمساعدة في كل خطوة على الطريق.

