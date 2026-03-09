from fastapi import FastAPI, Request # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
import requests
import os
from datetime import datetime

app = FastAPI()

# Разрешаем запросы с фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

@app.get("/")
async def root():
    return {"status": "TechConf Bot API is running"}

@app.post("/webhook")
async def webhook(request: Request):
    """Получение сообщений от Telegram"""
    try:
        update = await request.json()
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")
            if text == "/start":
                await send_welcome(chat_id)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.post("/api/submit")
async def submit_registration(request: Request):
    """Обработка заявки из формы"""
    try:
        data = await request.json()
        
        message = f"""
🎫 <b>НОВАЯ ЗАЯВКА</b>

👤 <b>ФИО:</b> {data.get('name')}
📧 <b>Email:</b> {data.get('email')}
📱 <b>Телефон:</b> {data.get('phone')}
🎟️ <b>Билет:</b> {data.get('ticketType')}
🏢 <b>Компания:</b> {data.get('company', '-')}
💼 <b>Должность:</b> {data.get('position', '-')}
🍽️ <b>Питание:</b> {data.get('dietary', '-')}

🔗 <b>Telegram:</b> @{data.get('telegram_username', 'нет')}
⏰ <b>Время:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}
        """
        
        await send_message(ADMIN_CHAT_ID, message)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

async def send_welcome(chat_id):
    webapp_url = os.getenv("WEBAPP_URL", "")
    keyboard = {
        "inline_keyboard": [[
            {"text": "📱 Открыть приложение", "web_app": {"url": webapp_url}}
        ]]
    }
    await send_message(
        chat_id,
        "🚀 <b>TechConf 2026</b>\n\nКонференция будущих технологий!\n📅 15-16 Мая 2026\n\nНажмите кнопку ниже 👇",
        keyboard
    )

async def send_message(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        data["reply_markup"] = requests.utils.to_json(reply_markup)
    requests.post(url, json=data)