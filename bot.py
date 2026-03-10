import logging
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

from config.settings import Settings

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

settings = Settings()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    try:
        keyboard = [[
            InlineKeyboardButton(
                text="📅 Открыть расписание",
                web_app=WebAppInfo(url=settings.WEBAPP_URL)
            )
        ]]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"Добро пожаловать на {settings.FORUM_NAME}! 👋\n"
            "Нажмите кнопку, чтобы открыть расписание.",
            reply_markup=reply_markup
        )
        
        logger.info(f"User {update.effective_user.id} started the bot")
        
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await update.message.reply_text(
            "Извините, произошла ошибка. Пожалуйста, попробуйте позже."
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    try:
        help_text = (
            "Доступные команды:\n"
            "/start - Запустить бота\n"
            "/help - Показать эту справку\n\n"
            "Нажмите на кнопку 'Открыть расписание' чтобы перейти в веб-приложение."
        )
        
        await update.message.reply_text(help_text)
        
    except Exception as e:
        logger.error(f"Error in help command: {e}")
        await update.message.reply_text("Произошла ошибка при обработке команды.")


async def post_init(application: Application):
    """Post initialization callback"""
    logger.info("Bot initialized successfully")


def main():
    """Main entry point"""
    try:
        settings.validate()
        
        application = Application.builder() \
            .token(settings.TELEGRAM_BOT_TOKEN) \
            .post_init(post_init) \
            .build()
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        
        logger.info("Bot is starting...")
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        exit(1)


if __name__ == "__main__":
    main()
