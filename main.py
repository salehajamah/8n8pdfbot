
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
import openai
import telegram
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, PreCheckoutQueryHandler
import logging
import asyncio
import json
import uuid
import redis
from fpdf import FPDF

# Load environment variables from .env file
load_dotenv()

# --- Configuration --- #
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEB_APP_URL = os.getenv("WEB_APP_URL")
PORT = int(os.getenv("PORT", 8000))
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
TELEGRAM_PROVIDER_TOKEN = os.getenv("TELEGRAM_PROVIDER_TOKEN")

# --- Initialize Components --- #
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates for HTML responses (not used directly for WebApp, but good practice)
templates = Jinja2Templates(directory="static")

# Configure logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

# Initialize Redis for caching and rate limiting
try:
    redis_client = redis.from_url(REDIS_URL)
    redis_client.ping() # Test connection
    logger.info("Successfully connected to Redis!")
except redis.exceptions.ConnectionError as e:
    logger.error(f"Could not connect to Redis: {e}. Caching and rate limiting will be disabled.")
    redis_client = None

# Initialize Telegram Bot
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
bot = application.bot

# --- In-memory storage for rate limiting (for demonstration, use Redis for production) ---
# For persistent rate limiting and usage tracking, Redis should be used.
# This dictionary will be used if redis_client is None.
user_requests_in_memory = {}

# --- Pydantic Models for Request Validation --- #
class ContentRequest(BaseModel):
    mainTopic: str = Field(..., min_length=3, max_length=200, description="الموضوع الرئيسي للمحتوى")
    contentType: str = Field(..., description="نوع المحتوى المطلوب (مطوية، بحث، ملخص، خطة عمل، إلخ)")
    contentLength: str = Field(..., description="طول المحتوى المطلوب (موجز جداً، مختصر، متوسط، مفصل، شامل)")
    styleOptions: Optional[Dict[str, bool]] = Field(default_factory=dict, description="خيارات الأسلوب (إيموجي، لغة بسيطة، أكاديمية، إلخ)")
    customFields: Optional[Dict[str, str]] = Field(default_factory=dict, description="حقول مخصصة إضافية من المستخدم")
    telegram_chat_id: Optional[int] = Field(None, description="معرف الدردشة الخاص بالمستخدم في تليجرام")
    telegram_user_id: Optional[int] = Field(None, description="معرف المستخدم الخاص بالمستخدم في تليجرام")

    @validator("mainTopic")
    def validate_topic_content(cls, v):
        if not v.strip():
            raise ValueError("الموضوع الرئيسي لا يمكن أن يكون فارغاً.")
        return v

    @validator("contentType")
    def validate_content_type(cls, v):
        valid_types = ["مطوية", "بحث", "ملخص", "خطة عمل", "محتوى لوسائل التواصل الاجتماعي"]
        if v not in valid_types:
            raise ValueError(f"نوع المحتوى غير صالح. الأنواع المتاحة: {", ".join(valid_types)}")
        return v

    @validator("contentLength")
    def validate_content_length(cls, v):
        valid_lengths = ["موجز جداً", "مختصر", "متوسط", "مفصل", "شامل"]
        if v not in valid_lengths:
            raise ValueError(f"طول المحتوى غير صالح. الأطوال المتاحة: {", ".join(valid_lengths)}")
        return v

# --- Helper Functions --- #
async def generate_openai_content(prompt: str, model: str = "gpt-3.5-turbo", temperature: float = 0.7, max_tokens: int = 1000) -> str:
    try:
        response = await openai.ChatCompletion.acreate(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise HTTPException(status_code=500, detail=f"خطأ في خدمة الذكاء الاصطناعي: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred during OpenAI call: {e}")
        raise HTTPException(status_code=500, detail="حدث خطأ غير متوقع أثناء توليد المحتوى.")

async def get_user_daily_requests(user_id: int) -> int:
    if redis_client:
        key = f"user_requests:{user_id}:daily"
        count = await redis_client.get(key)
        return int(count) if count else 0
    else:
        return user_requests_in_memory.get(user_id, 0)

async def increment_user_daily_requests(user_id: int):
    if redis_client:
        key = f"user_requests:{user_id}:daily"
        await redis_client.incr(key)
        # Set expiry to end of day (assuming UTC for simplicity)
        # This requires more complex logic for exact end-of-day in user"s timezone
        # For now, a simple expiry (e.g., 24 hours) or daily cron job to reset is better
        if await redis_client.ttl(key) == -1:
            await redis_client.expire(key, 24 * 60 * 60) # Expires in 24 hours
    else:
        user_requests_in_memory[user_id] = user_requests_in_memory.get(user_id, 0) + 1

async def get_cached_content(prompt_hash: str) -> Optional[str]:
    if redis_client:
        content = await redis_client.get(f"cache:{prompt_hash}")
        return content.decode() if content else None
    return None

async def set_cached_content(prompt_hash: str, content: str):
    if redis_client:
        await redis_client.set(f"cache:{prompt_hash}", content, ex=3600) # Cache for 1 hour

async def generate_pdf(html_content: str, is_free_version: bool = True) -> bytes:
    # إزالة العلامة المائية للنسخة المدفوعة
    if not is_free_version:
        html_content = html_content.replace("<div class=\"watermark\">نسخة مجانية</div>", "")

    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        # إدراج النص فقط من html_content (يمكنك تحسين ذلك لاحقاً)
        # إذا كان html_content يحتوي على وسوم HTML، يمكن استخدام مكتبة مثل BeautifulSoup لاستخلاص النص فقط
        import re
        text = re.sub('<[^<]+?>', '', html_content)
        pdf.multi_cell(0, 10, txt=text)
        import io
        pdf_bytes = io.BytesIO()
        pdf.output(pdf_bytes)
        pdf_bytes.seek(0)
        return pdf_bytes.read()
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        raise HTTPException(status_code=500, detail="حدث خطأ أثناء توليد ملف PDF.")

# --- Telegram Bot Handlers --- #
async def start_command(update: Update, context: telegram.ext.CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("🚀 ابدأ مشروعًا جديدًا", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "مرحبًا بك في منشئ المحتوى الذكي! اضغط على الزر أدناه لبدء إنشاء مطوية أو بحث جديد.",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: telegram.ext.CallbackContext) -> None:
    # This handler is primarily for receiving WebApp data
    if update.effective_message.web_app_data:
        web_app_data = update.effective_message.web_app_data.data
        logger.info(f"Received WebApp data: {web_app_data}")
        # Process the data (e.g., send to FastAPI endpoint or directly generate content)
        # For this architecture, WebApp data is sent to FastAPI via /generate-content
        # and then the PDF is sent back to the user via the bot.
        await update.effective_message.reply_text("تم استلام بياناتك. جاري معالجة طلبك...")
    else:
        await update.message.reply_text('أنا بوت لإنشاء المحتوى. يرجى استخدام زر "ابدأ مشروعًا جديدًا" لبدء العمل.')

async def pre_checkout_callback(update: Update, context: telegram.ext.CallbackContext) -> None:
    query = update.pre_checkout_query
    if query.invoice_payload != "brochure_premium_content":
        await query.answer(ok=False, error_message="حدث خطأ في عملية الدفع.")
    else:
        await query.answer(ok=True)

async def successful_payment_callback(update: Update, context: telegram.ext.CallbackContext) -> None:
    logger.info("Payment successful!")
    # Here you would typically unlock premium features for the user
    # For now, just acknowledge the payment
    await update.message.reply_text("شكراً لك! تم الدفع بنجاح. يمكنك الآن إنشاء محتوى مميز.")

# --- FastAPI Endpoints --- #
# عرض الصفحة الرئيسية عند زيارة / بدون التأثير على بقية المشروع
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.on_event("startup")
async def startup_event():
    # Set up Telegram webhook
    webhook_url = f"{WEB_APP_URL}/telegram-webhook"
    await bot.set_webhook(url=webhook_url)
    logger.info(f"Telegram webhook set to: {webhook_url}")

    # Start Telegram bot polling in background if webhook is not set
    # This is primarily for local development without public URL
    if not WEB_APP_URL:
        logger.warning("WEB_APP_URL is not set. Telegram bot will use polling. This is not recommended for production.")
        asyncio.create_task(application.run_polling())

@app.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    update = Update.de_json(await request.json(), bot)
    await application.update_queue.put(update)
    return "ok"

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "AI Content Creator is running!"}

@app.post("/generate-content")
async def generate_content_endpoint(request_data: ContentRequest, background_tasks: BackgroundTasks):
    logger.info(f"Received content generation request: {request_data.dict()}")

    user_id = request_data.telegram_user_id
    chat_id = request_data.telegram_chat_id

    # --- Rate Limiting / Usage Monitoring --- #
    if user_id:
        current_requests = await get_user_daily_requests(user_id)
        if request_data.contentLength != "موجز جداً" and current_requests >= 1: # Allow 1 free brief content per day
            # For paid features, we will prompt for payment
            if TELEGRAM_PROVIDER_TOKEN and chat_id:
                price = 100 # Example price in smallest currency units (e.g., cents)
                title = "محتوى مميز"
                description = f"الحصول على محتوى {request_data.contentLength} حول {request_data.mainTopic}"
                payload = "brochure_premium_content"
                currency = "XTR" # Telegram Stars currency

                # Send invoice to user
                await bot.send_invoice(
                    chat_id=chat_id,
                    title=title,
                    description=description,
                    payload=payload,
                    provider_token=TELEGRAM_PROVIDER_TOKEN,
                    currency=currency,
                    prices=[telegram.LabeledPrice(label=title, amount=price)],
                    start_parameter="premium_content",
                    need_name=False, need_phone_number=False, need_email=False, need_shipping_address=False,
                    send_email_to_provider=False, send_phone_number_to_provider=False,
                    is_flexible=False,
                )
                return {"status": "payment_required", "message": "يرجى إتمام عملية الدفع للحصول على المحتوى المميز.", "invoice_sent": True}
            else:
                raise HTTPException(status_code=402, detail="هذه الميزة تتطلب دفعاً. يرجى ترقية اشتراكك أو استخدام المحتوى الموجز المجاني.")
        
        await increment_user_daily_requests(user_id)

    # --- Construct OpenAI Prompt --- #
    prompt_parts = [
        f"الرجاء توليد {request_data.contentType} حول الموضوع التالي: {request_data.mainTopic}.\n",
        f"الطول المطلوب: {request_data.contentLength}.\n"
    ]

    if request_data.styleOptions:
        if request_data.styleOptions.get("useEmoji"): prompt_parts.append("استخدم الرموز التعبيرية (إيموجي) بشكل مناسب.\n")
        if request_data.styleOptions.get("simpleLanguage"): prompt_parts.append("استخدم لغة بسيطة ومباشرة.\n")
        if request_data.styleOptions.get("academicLanguage"): prompt_parts.append("استخدم لغة أكاديمية ورسمية.\n")
        if request_data.styleOptions.get("bulletPoints"): prompt_parts.append("نظم المحتوى على شكل نقاط رئيسية.\n")
        if request_data.styleOptions.get("discussionQuestions"): prompt_parts.append("أضف أسئلة للمناقشة في نهاية المحتوى.\n")

    if request_data.customFields:
        for key, value in request_data.customFields.items():
            prompt_parts.append(f"{key}: {value}.\n")

    full_prompt = "".join(prompt_parts).strip()
    logger.info(f"Generated OpenAI prompt: {full_prompt}")

    # --- Caching --- #
    prompt_hash = str(hash(full_prompt))
    cached_content = await get_cached_content(prompt_hash)
    if cached_content:
        generated_content = cached_content
        logger.info("Content served from cache.")
    else:
        # --- Generate Content with OpenAI --- #
        generated_content = await generate_openai_content(full_prompt)
        await set_cached_content(prompt_hash, generated_content)
        logger.info("Content generated by OpenAI and cached.")

    # --- Generate PDF --- #
    # Load the HTML template
    with open("static/pdf_template.html", "r", encoding="utf-8") as f:
        html_template = f.read()

    # Replace placeholder with generated content
    final_html = html_template.replace("{{GENERATED_CONTENT}}", generated_content)

    # Determine if it"s a free version (brief content)
    is_free_version = (request_data.contentLength == "موجز جداً")

    pdf_bytes = await generate_pdf(final_html, is_free_version=is_free_version)

    # --- Send PDF back to Telegram User --- #
    if chat_id:
        try:
            # Generate a unique filename
            filename = f"content_{uuid.uuid4().hex}.pdf"
            # Save PDF to a temporary file (or directly send bytes if telegram-bot supports it)
            with open(filename, "wb") as f:
                f.write(pdf_bytes)
            
            await bot.send_document(chat_id=chat_id, document=open(filename, "rb"), caption="المحتوى المطلوب جاهز!")
            os.remove(filename) # Clean up temporary file
            logger.info(f"PDF sent to chat_id {chat_id}")
        except Exception as e:
            logger.error(f"Error sending PDF to Telegram: {e}")
            # Fallback to sending a message if PDF sending fails
            await bot.send_message(chat_id=chat_id, text="عذراً، حدث خطأ أثناء إرسال ملف PDF. يرجى المحاولة مرة أخرى.")
            raise HTTPException(status_code=500, detail="حدث خطأ أثناء إرسال ملف PDF إلى تليجرام.")

    return {"status": "success", "message": "تم توليد المحتوى وإرساله بنجاح!"}

# --- Telegram Bot Setup --- #
application.add_handler(CommandHandler("start", start_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
application.add_handler(PreCheckoutQueryHandler(pre_checkout_callback))
application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))

# --- Run FastAPI App --- #
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)



