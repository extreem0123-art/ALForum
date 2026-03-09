from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton(
            text="📅 Открыть расписание",
            web_app=WebAppInfo(url="https://al-forum.vercel.app/")
        )
    ]]
    await update.message.reply_text(
        "Добро пожаловать на TechConf 2026! 👋\nНажмите кнопку, чтобы открыть расписание.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

app = ApplicationBuilder().token("8607589730:AAF-HI8oLCsPBz10LDSl506D96Vy3h2d0rw").build()
app.add_handler(CommandHandler("start", start))
app.run_polling()