# سكريبت PowerShell للتبديل السريع بين حسابات Git
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("salehajamah", "salehajamah-hue", "Salehmalki")]
    [string]$Account
)

switch ($Account) {
    "salehajamah" {
        git config user.name "salehajamah"
        git config user.email "salehajamah@gmail.com"
        Write-Host "تم التبديل إلى حساب: salehajamah" -ForegroundColor Green
    }
    "salehajamah-hue" {
        git config user.name "salehajamah-hue"
        git config user.email "salehajamah@gmail.com"
        Write-Host "تم التبديل إلى حساب: salehajamah-hue" -ForegroundColor Green
    }
    "Salehmalki" {
        git config user.name "Salehmalki"
        git config user.email "wzxwzx35@gmail.com"
        Write-Host "تم التبديل إلى حساب: Salehmalki" -ForegroundColor Green
    }
}

Write-Host "اسم المستخدم الحالي: $(git config user.name)" -ForegroundColor Yellow
Write-Host "البريد الإلكتروني الحالي: $(git config user.email)" -ForegroundColor Yellow
