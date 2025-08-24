# منشئ المحتوى الذكي - AI Content Creator Bot

بوت تليجرام متطور لإنشاء المحتوى التعليمي والأكاديمي باستخدام الذكاء الاصطناعي، مع واجهة ويب تفاعلية وتحويل احترافي إلى PDF.

## الميزات الرئيسية

### 🤖 إنشاء محتوى ذكي
- **أنواع المحتوى المدعومة:**
  - مطويات تعليمية
  - أبحاث مدرسية
  - ملخصات للكتب
  - خطط عمل للمشاريع
  - محتوى لوسائل التواصل الاجتماعي

### 🎨 خيارات التخصيص المتقدمة
- **أحجام المحتوى:** موجز جدًا (مجاني)، مختصر، متوسط، مفصل، شامل
- **خيارات الأسلوب:**
  - استخدام الرموز التعبيرية (إيموجي)
  - لغة بسيطة ومباشرة
  - لغة أكاديمية ورسمية
  - تنظيم على شكل نقاط رئيسية
  - إضافة أسئلة للمناقشة

### 📱 واجهة ويب تفاعلية
- تصميم متجاوب يدعم جميع الأجهزة
- تكامل كامل مع Telegram WebApp
- إضافة حقول مخصصة ديناميكيًا
- واجهة باللغة العربية مع دعم RTL

### 📄 تحويل احترافي إلى PDF
- قالب PDF متقدم مع دعم الخطوط العربية
- تنسيق احترافي مع رؤوس وتذييلات
- دعم العلامات المائية للنسخ المجانية
- تحسين للطباعة والعرض الرقمي

## التقنيات المستخدمة

- **Backend:** FastAPI + Python
- **AI Integration:** OpenAI GPT-3.5-turbo
- **Telegram Bot:** python-telegram-bot
- **PDF Generation:** WeasyPrint
- **Frontend:** HTML5 + CSS3 + JavaScript
- **Deployment:** Render.com

## متطلبات التشغيل

### المتغيرات البيئية المطلوبة
```bash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
WEB_APP_URL=https://your-app.onrender.com
PORT=8000
```

### المكتبات المطلوبة
```bash
pip install -r requirements.txt
```

## طريقة التشغيل

### 1. التشغيل المحلي
```bash
# تثبيت المكتبات
pip install -r requirements.txt

# تشغيل الخادم
python main.py
```

### 2. النشر على Render
1. ربط المستودع بـ Render
2. إضافة المتغيرات البيئية
3. تعيين أمر البناء: `pip install -r requirements.txt`
4. تعيين أمر التشغيل: `python main.py`

## إعداد البوت

### 1. إنشاء بوت تليجرام
1. تحدث مع @BotFather على تليجرام
2. استخدم الأمر `/newbot`
3. احفظ الـ Token المُعطى

### 2. إعداد WebApp
1. استخدم الأمر `/newapp` مع @BotFather
2. اربط WebApp بالبوت
3. حدد URL التطبيق المنشور

### 3. إعداد Webhook
بعد النشر، قم بتعيين webhook للبوت:
```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_APP_URL>/telegram-webhook"
```

## هيكل المشروع

```
brochure-bot/
├── main.py                 # الملف الرئيسي للتطبيق
├── requirements.txt        # المكتبات المطلوبة
├── README.md              # دليل المشروع
├── .gitignore             # ملفات Git المتجاهلة
└── static/                # الملفات الثابتة
    ├── index.html         # الواجهة الرئيسية
    ├── style.css          # ملف التنسيق
    ├── script.js          # منطق JavaScript
    ├── pdf_template.html  # قالب PDF
    ├── privacy.html       # سياسة الخصوصية
    └── contact.html       # صفحة التواصل
```

## API Endpoints

### الواجهات العامة
- `GET /` - الصفحة الرئيسية
- `GET /privacy.html` - سياسة الخصوصية
- `GET /contact.html` - صفحة التواصل
- `GET /health` - فحص حالة الخدمة

### واجهات التطبيق
- `POST /generate-content` - إنشاء المحتوى
- `POST /telegram-webhook` - استقبال تحديثات تليجرام

## الأمان والخصوصية

- تشفير جميع الاتصالات عبر HTTPS
- عدم تخزين البيانات الشخصية
- استخدام آمن لـ APIs الخارجية
- سياسة خصوصية واضحة ومفصلة

## الدعم والمساهمة

للحصول على الدعم أو المساهمة في تطوير المشروع، يرجى:
- فتح Issue جديد للمشاكل أو الاقتراحات
- إرسال Pull Request للتحسينات
- التواصل عبر معلومات الاتصال في التطبيق

## الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف LICENSE للتفاصيل.

---

**تم تطوير هذا المشروع بواسطة Manus AI**



