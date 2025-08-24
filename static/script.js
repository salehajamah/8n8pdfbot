document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contentForm');
    const addFieldButton = document.getElementById('addAdditionalField');
    const customFieldsContainer = document.getElementById('additionalFields');
    const statusMessage = document.getElementById('statusMessage');
    const telegramUser = Telegram.WebApp.initDataUnsafe.user;
    const telegramChat = Telegram.WebApp.initDataUnsafe.chat;

    // Set Telegram user/chat IDs if available
    if (telegramUser) {
        document.getElementById('telegramUserId').value = telegramUser.id;
    }
    if (telegramChat) {
        document.getElementById('telegramChatId').value = telegramChat.id;
    }

    // Populate content type dropdown
    const contentTypes = ["مطوية", "بحث مدرسي", "ملخص لكتاب", "خطة عمل لمشروع", "محتوى لمنشور على وسائل التواصل الاجتماعي"];
    const contentTypeSelect = document.getElementById('outputType');
    contentTypes.forEach(type => {
        const option = document.createElement('option');
        option.value = type;
        option.textContent = type;
        contentTypeSelect.appendChild(option);
    });

    // Populate content length dropdown
    const contentLengths = ["موجز جدًا", "مختصر", "متوسط", "مفصل", "شامل"];
    const contentLengthSelect = document.getElementById('contentLength');
    contentLengths.forEach(length => {
        const option = document.createElement('option');
        option.value = length;
        option.textContent = length;
        contentLengthSelect.appendChild(option);
    });

    // Add custom field functionality
    addFieldButton.addEventListener('click', function() {
        const fieldGroup = document.createElement('div');
        fieldGroup.classList.add('custom-field-group');
        fieldGroup.style.marginBottom = '10px';
        fieldGroup.style.padding = '10px';
        fieldGroup.style.border = '1px solid #ddd';
        fieldGroup.style.borderRadius = '5px';
        fieldGroup.style.backgroundColor = '#f9f9f9';
        
        fieldGroup.innerHTML = `
            <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
                <input type="text" class="custom-field-label" placeholder="اسم الحقل (مثال: الصف)" style="flex: 1; min-width: 150px;">
                <input type="text" class="custom-field-value" placeholder="قيمة الحقل (مثال: الثالث الابتدائي)" style="flex: 1; min-width: 150px;">
                <button type="button" class="remove-field-button" style="background: #ff4444; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer;">إزالة</button>
            </div>
        `;
        customFieldsContainer.appendChild(fieldGroup);

        fieldGroup.querySelector('.remove-field-button').addEventListener('click', function() {
            fieldGroup.remove();
        });
    });

    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        statusMessage.textContent = 'جاري إرسال طلبك...';
        statusMessage.style.color = 'blue';

        const mainTopic = document.getElementById('mainTopic').value;
        const contentType = document.getElementById('outputType').value;
        const contentLength = document.getElementById('contentLength').value;
        const telegramChatId = document.getElementById('telegramChatId').value;
        const telegramUserId = document.getElementById('telegramUserId').value;

        const styleOptions = {
            useEmoji: document.getElementById('useEmoji').checked,
            simpleLanguage: document.getElementById('simpleLanguage').checked,
            academicLanguage: document.getElementById('academicLanguage').checked,
            bulletPoints: document.getElementById('bulletPoints').checked,
            discussionQuestions: document.getElementById('discussionQuestions').checked
        };

        const customFields = {};
        document.querySelectorAll('.custom-field-group').forEach(group => {
            const label = group.querySelector('.custom-field-label').value;
            const value = group.querySelector('.custom-field-value').value;
            if (label && value) {
                customFields[label] = value;
            }
        });

        const requestData = {
            mainTopic: mainTopic,
            contentType: contentType,
            contentLength: contentLength,
            styleOptions: styleOptions,
            customFields: customFields,
            telegram_chat_id: parseInt(telegramChatId),
            telegram_user_id: parseInt(telegramUserId)
        };

        try {
            console.log('Sending request:', requestData);
            const response = await fetch('/generate-content', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });

            console.log('Response status:', response.status);
            const result = await response.json();
            console.log('Response result:', result);

            if (response.ok) {
                statusMessage.textContent = 'تم إرسال طلبك بنجاح! تحقق من بوت تليجرام الخاص بك للحصول على المحتوى.';
                statusMessage.style.color = 'green';
                
                // Close WebApp after a short delay to show success message
                setTimeout(() => {
                    if (window.Telegram && window.Telegram.WebApp) {
                        window.Telegram.WebApp.close();
                    }
                }, 2000);
            } else if (response.status === 402 && result.invoice_sent) {
                statusMessage.textContent = 'يرجى إتمام عملية الدفع في تليجرام للحصول على المحتوى المميز.';
                statusMessage.style.color = 'orange';
                if (result.invoice_url && window.Telegram && window.Telegram.WebApp) {
                    window.Telegram.WebApp.openInvoice(result.invoice_url);
                }
            } else {
                statusMessage.textContent = `خطأ: ${result.detail || result.message || 'حدث خطأ غير معروف.'}`;
                statusMessage.style.color = 'red';
            } 
        } catch (error) {
            console.error('Error:', error);
            statusMessage.textContent = 'حدث خطأ في الاتصال بالخادم. يرجى المحاولة مرة أخرى.';
            statusMessage.style.color = 'red';
        }
    });
});
