import logging
import os
from typing import Dict, Any

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext

from config.settings import Settings

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class TechConfBot:
    def __init__(self):
        self.settings = Settings()
        self.settings.validate()
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        try:
            keyboard = [[
                InlineKeyboardButton(
                    text="📅 Открыть расписание",
                    web_app=WebAppInfo(url=self.settings.WEBAPP_URL)
                )
            ]]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "Добро пожаловать на TechConf 2026! 👋\n"
                "Нажмите кнопку, чтобы открыть расписание.",
                reply_markup=reply_markup
            )
            
            logger.info(f"User {update.effective_user.id} started the bot")
            
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            await update.message.reply_text(
                "Извините, произошла ошибка. Пожалуйста, попробуйте позже."
            )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    
    def run(self):
        """Run the bot"""
        try:
            app = ApplicationBuilder().token(self.settings.TELEGRAM_BOT_TOKEN).build()
            
            # Add handlers
            app.add_handler(CommandHandler("start", self.start))
            app.add_handler(CommandHandler("help", self.help_command))
            
            logger.info("Bot is starting...")
            app.run_polling()
            
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            raise


def main():
    """Main entry point"""
    try:
        bot = TechConfBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        exit(1)


if __name__ == "__main__":
    main()