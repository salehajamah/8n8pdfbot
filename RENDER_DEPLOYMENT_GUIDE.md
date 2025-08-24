# دليل نشر المشروع على Render

## الخطوات:

### 1. إعداد بوت تليجرام
1. تحدث مع @BotFather على تليجرام
2. استخدم الأمر `/newbot`
3. اختر اسم للبوت
4. احفظ الـ Token المُعطى

### 2. إعداد OpenAI API
1. اذهب إلى: https://platform.openai.com/api-keys
2. أنشئ مفتاح API جديد
3. انسخ المفتاح

### 3. نشر المشروع على Render

#### أ. الذهاب إلى Render
- اذهب إلى: https://render.com
- سجل دخول باستخدام GitHub

#### ب. إنشاء خدمة جديدة
1. انقر على "New +"
2. اختر "Web Service"
3. اربط حساب GitHub
4. اختر المستودع: `salehajamah/8n8pdfbot`

#### ج. إعداد الخدمة
- **Name:** `brochure-bot`
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python main.py`

#### د. إضافة المتغيرات البيئية
في قسم "Environment Variables"، أضف:

| Key | Value | Description |
|-----|-------|-------------|
| `TELEGRAM_BOT_TOKEN` | `your_bot_token_here` | رمز بوت تليجرام |
| `OPENAI_API_KEY` | `your_openai_api_key_here` | مفتاح OpenAI API |
| `WEB_APP_URL` | `https://your-app-name.onrender.com` | رابط التطبيق (سيتم تعيينه تلقائياً) |
| `PORT` | `8000` | المنفذ (سيتم تعيينه تلقائياً) |

### 4. إعداد Webhook للبوت
بعد النشر، قم بتعيين webhook للبوت:

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://your-app-name.onrender.com/telegram-webhook"
```

### 5. إعداد WebApp في تليجرام
1. تحدث مع @BotFather
2. استخدم الأمر `/newapp`
3. اختر البوت
4. أدخل عنوان URL: `https://your-app-name.onrender.com`

## ملاحظات مهمة:

### ✅ الملفات المطلوبة (موجودة بالفعل):
- `render.yaml` - إعدادات Render
- `requirements.txt` - المكتبات المطلوبة
- `main.py` - التطبيق الرئيسي
- `static/` - الملفات الثابتة

### ⚠️ المتغيرات البيئية المطلوبة:
- `TELEGRAM_BOT_TOKEN` - **مطلوب**
- `OPENAI_API_KEY` - **مطلوب**
- `WEB_APP_URL` - سيتم تعيينه تلقائياً
- `PORT` - سيتم تعيينه تلقائياً

### 🔧 إعدادات إضافية:
- **Auto-Deploy:** مفعل (سيتم النشر تلقائياً عند تحديث GitHub)
- **Health Check Path:** `/health`

## اختبار التطبيق:

### 1. فحص حالة الخدمة:
```
https://your-app-name.onrender.com/health
```

### 2. الواجهة الرئيسية:
```
https://your-app-name.onrender.com/
```

### 3. اختبار البوت:
- ابحث عن البوت على تليجرام
- استخدم الأمر `/start`
- انقر على "إنشاء محتوى"

## حل المشاكل الشائعة:

### إذا فشل البناء:
- تحقق من `requirements.txt`
- تأكد من صحة `main.py`

### إذا فشل التشغيل:
- تحقق من المتغيرات البيئية
- راجع سجلات Render

### إذا لم يعمل البوت:
- تحقق من `TELEGRAM_BOT_TOKEN`
- تأكد من إعداد Webhook
- راجع سجلات التطبيق

## روابط مفيدة:
- [Render Documentation](https://render.com/docs)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [OpenAI API Documentation](https://platform.openai.com/docs)
