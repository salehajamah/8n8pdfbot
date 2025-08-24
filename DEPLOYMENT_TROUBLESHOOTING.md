# دليل حل مشاكل النشر على Render

## المشكلة: خطأ في تثبيت المكتبات

### الخطأ:
```
error: failed to solve: process "/bin/sh -c apt-get update && apt-get install -y ..." did not complete successfully: exit code: 100
```

### الحل:
تم تحديث ملف `requirements.txt` لإزالة `weasyprint` واستبداله بـ `fpdf2` الذي لا يحتاج إلى مكتبات نظام معقدة.

## التغييرات التي تمت:

### 1. تحديث requirements.txt:
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-telegram-bot==20.7
openai==1.3.7
fpdf2==2.7.6  # بدلاً من weasyprint
python-multipart==0.0.6
redis==5.0.1
python-dotenv==1.0.0
jinja2==3.1.2
aiofiles==23.2.1
```

### 2. تبسيط render.yaml:
```yaml
buildCommand: pip install -r requirements.txt
```

## خطوات النشر المحدثة:

### 1. إعادة النشر على Render:
1. اذهب إلى لوحة تحكم Render
2. اختر مشروعك
3. انقر على "Manual Deploy"
4. اختر "Deploy latest commit"

### 2. إذا استمرت المشكلة:
- استخدم ملف `Dockerfile.alternative` الموجود
- أو جرب منصة نشر أخرى مثل Railway أو Heroku

## منصات نشر بديلة:

### 1. Railway:
- اذهب إلى: https://railway.app
- اربط حساب GitHub
- اختر المستودع
- أضف المتغيرات البيئية

### 2. Heroku:
- اذهب إلى: https://heroku.com
- اربط حساب GitHub
- اختر المستودع
- أضف المتغيرات البيئية

### 3. Vercel:
- اذهب إلى: https://vercel.com
- اربط حساب GitHub
- اختر المستودع
- أضف المتغيرات البيئية

## نصائح إضافية:

### 1. تحقق من السجلات:
- راجع سجلات البناء في Render
- ابحث عن أخطاء محددة

### 2. اختبر محلياً:
```bash
pip install -r requirements.txt
python main.py
```

### 3. تحقق من المتغيرات البيئية:
- تأكد من إضافة `TELEGRAM_BOT_TOKEN`
- تأكد من إضافة `OPENAI_API_KEY`

## إذا لم تعمل الحلول:

### 1. استخدم Dockerfile:
```bash
# استخدم Dockerfile.alternative
docker build -f Dockerfile.alternative -t brochure-bot .
docker run -p 8000:8000 brochure-bot
```

### 2. جرب منصة أخرى:
- Railway (أسهل)
- Heroku (أكثر استقراراً)
- Vercel (سريع)

### 3. اتصل بالدعم:
- Render Support: https://render.com/docs/help
- GitHub Issues: إذا كانت المشكلة في الكود
