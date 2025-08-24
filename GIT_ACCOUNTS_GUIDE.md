# دليل إدارة حسابات Git المتعددة

## الحسابات المتاحة:
1. **salehajamah** - salehajamah@gmail.com
2. **salehajamah-hue** - salehajamah@gmail.com  
3. **Salehmalki** - wzxwzx35@gmail.com

## الطريقة السريعة للتبديل:

### 1. التبديل إلى حساب salehajamah:
```bash
git config user.name "salehajamah"
git config user.email "salehajamah@gmail.com"
```

### 2. التبديل إلى حساب salehajamah-hue:
```bash
git config user.name "salehajamah-hue"
git config user.email "salehajamah@gmail.com"
```

### 3. التبديل إلى حساب Salehmalki:
```bash
git config user.name "Salehmalki"
git config user.email "wzxwzx35@gmail.com"
```

## خطوات الدفع للمرة القادمة:

### 1. إعداد المشروع:
```bash
git init
git add .
git commit -m "Initial commit"
```

### 2. تحديد الحساب المطلوب:
```bash
# اختر الحساب المناسب من القائمة أعلاه
```

### 3. إضافة Remote Repository:
```bash
git remote add origin https://github.com/[USERNAME]/[REPO-NAME].git
```

### 4. الدفع:
```bash
git push -u origin main
# أدخل اسم المستخدم وكلمة المرور أو Personal Access Token
```

## حل مشاكل الصلاحيات:

### إذا واجهت مشكلة 403:
```bash
# حذف بيانات الاعتماد المخزنة
cmdkey /delete:git:https://github.com

# أو حذف إعدادات Credential Helper
git config --global --unset credential.helper
```

### إعادة تعيين Credential Helper:
```bash
git config --global credential.helper manager-core
```

## نصائح مهمة:

1. **استخدم Personal Access Token** بدلاً من كلمة المرور
2. **احتفظ بقائمة الحسابات** في ملف منفصل
3. **تحقق من الحساب الحالي** قبل الدفع:
   ```bash
   git config user.name
   git config user.email
   ```
4. **استخدم SSH Keys** للحسابات المتعددة (متقدم)

## استخدام السكريبت:
```bash
# تشغيل سكريبت التبديل
.\switch-git-account.ps1 -Account salehajamah
```
