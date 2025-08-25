document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contentForm');
    const addCustomFieldBtn = document.getElementById('addCustomField');
    const newCustomLabelInput = document.getElementById('newCustomLabel');
    const newCustomValueInput = document.getElementById('newCustomValue');
    const customFieldsList = document.getElementById('additionalFieldsList');
    const customFieldsState = [];
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
    const contentLengths = ["موجز جداً", "مختصر", "متوسط", "مفصل", "شامل"];
    const contentLengthSelect = document.getElementById('contentLength');
    contentLengths.forEach(length => {
        const option = document.createElement('option');
        option.value = length;
        option.textContent = length;
        contentLengthSelect.appendChild(option);
    });

    function renderCustomFields() {
        customFieldsList.innerHTML = '';
        customFieldsState.forEach((item, index) => {
            const row = document.createElement('div');
            row.classList.add('custom-field-row');
            row.style.display = 'flex';
            row.style.gap = '10px';
            row.style.alignItems = 'center';
            row.style.flexWrap = 'wrap';
            row.style.marginTop = '8px';

            const labelEl = document.createElement('input');
            labelEl.type = 'text';
            labelEl.value = item.label;
            labelEl.readOnly = true;
            labelEl.style.flex = '1';
            labelEl.style.minWidth = '150px';

            const valueEl = document.createElement('input');
            valueEl.type = 'text';
            valueEl.value = item.value;
            valueEl.readOnly = true;
            valueEl.style.flex = '1';
            valueEl.style.minWidth = '150px';

            const removeBtn = document.createElement('button');
            removeBtn.type = 'button';
            removeBtn.textContent = 'إزالة';
            removeBtn.addEventListener('click', function() {
                customFieldsState.splice(index, 1);
                renderCustomFields();
            });

            row.appendChild(labelEl);
            row.appendChild(valueEl);
            row.appendChild(removeBtn);
            customFieldsList.appendChild(row);
        });
    }

    addCustomFieldBtn.addEventListener('click', function() {
        const label = newCustomLabelInput.value.trim();
        const value = newCustomValueInput.value.trim();
        if (!label || !value) {
            statusMessage.textContent = 'يرجى إدخال اسم الحقل وقيمته قبل الإضافة.';
            statusMessage.style.color = 'red';
            return;
        }
        customFieldsState.push({ label, value });
        newCustomLabelInput.value = '';
        newCustomValueInput.value = '';
        statusMessage.textContent = '';
        renderCustomFields();
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
        customFieldsState.forEach(item => {
            customFields[item.label] = item.value;
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
            
            // Show loading state
            statusMessage.textContent = 'جاري إرسال طلبك...';
            statusMessage.style.color = 'blue';
            
            const response = await fetch('/generate-content', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });

            console.log('Response status:', response.status);
            let result = null;
            try {
                result = await response.json();
            } catch (_) {
                // ignore JSON parse errors; will fall back to status text
            }
            console.log('Response result:', result);

            if (response.ok && result && result.status === 'success') {
                statusMessage.textContent = 'تم إرسال طلبك بنجاح! تحقق من بوت تليجرام الخاص بك للحصول على المحتوى.';
                statusMessage.style.color = 'green';
                
                // Close WebApp after a short delay to show success message
                setTimeout(() => {
                    if (window.Telegram && window.Telegram.WebApp) {
                        window.Telegram.WebApp.close();
                    }
                }, 2000);
            } else if (response.status === 402 && result && result.invoice_sent) {
                statusMessage.textContent = 'يرجى إتمام عملية الدفع في تليجرام للحصول على المحتوى المميز.';
                statusMessage.style.color = 'orange';
                if (result.invoice_url && window.Telegram && window.Telegram.WebApp) {
                    window.Telegram.WebApp.openInvoice(result.invoice_url);
                }
            } else {
                const detail = (result && (result.detail || result.message)) || `HTTP ${response.status}`;
                statusMessage.textContent = `خطأ: ${detail}`;
                statusMessage.style.color = 'red';
            } 
        } catch (error) {
            console.error('Error:', error);
            statusMessage.textContent = 'حدث خطأ في الاتصال بالخادم. يرجى المحاولة مرة أخرى.';
            statusMessage.style.color = 'red';
        }
    });
});
