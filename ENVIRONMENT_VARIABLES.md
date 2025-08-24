# المتغيرات البيئية المطلوبة

## المتغيرات الأساسية (مطلوبة):

### 1. TELEGRAM_BOT_TOKEN
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```
**كيفية الحصول عليه:**
1. تحدث مع @BotFather على تليجرام
2. استخدم الأمر `/newbot`
3. اختر اسم للبوت
4. انسخ الـ Token المُعطى

### 2. OPENAI_API_KEY
```
OPENAI_API_KEY=your_openai_api_key_here
```
**كيفية الحصول عليه:**
1. اذهب إلى: https://platform.openai.com/api-keys
2. أنشئ مفتاح API جديد
3. انسخ المفتاح

## المتغيرات التلقائية (سيتم تعيينها تلقائياً على Render):

### 3. WEB_APP_URL
```
WEB_APP_URL=https://your-app-name.onrender.com
```
سيتم تعيينه تلقائياً بعد النشر على Render

### 4. PORT
```
PORT=8000
```
سيتم تعيينه تلقائياً على Render

## المتغيرات الاختيارية:

### 5. REDIS_URL
```
REDIS_URL=redis://localhost:6379/0
```
للتخزين المؤقت (اختياري)

### 6. TELEGRAM_PROVIDER_TOKEN
```
TELEGRAM_PROVIDER_TOKEN=your_provider_token_here
```
للمدفوعات (اختياري)

## كيفية إضافة المتغيرات على Render:

1. اذهب إلى لوحة تحكم Render
2. اختر مشروعك
3. اذهب إلى "Environment"
4. أضف المتغيرات المطلوبة
5. احفظ التغييرات
6. أعد تشغيل الخدمة
