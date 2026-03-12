"""
Telegram Bot for ALFA LIGHT FORUM 2026
Provides information about schedule, speakers, FAQ, and venue.
"""

import json
import logging
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters

from config.settings import Settings

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

settings = Settings()

# Path to data files
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "static" / "data"


def load_json_data(filename: str) -> dict | list:
    """Load JSON data from file"""
    try:
        filepath = DATA_DIR / filename
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {filename}: {e}")
        return {}


def get_main_keyboard() -> InlineKeyboardMarkup:
    """Create main navigation keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("📅 Расписание", callback_data="schedule"),
            InlineKeyboardButton("🎤 Спикеры", callback_data="speakers")
        ],
        [
            InlineKeyboardButton("❓ FAQ", callback_data="faq"),
            InlineKeyboardButton("📍 Площадка", callback_data="venue")
        ],
        [
            InlineKeyboardButton(
                "🌐 Открыть сайт",
                web_app=WebAppInfo(url=settings.WEBAPP_URL)
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: CallbackContext):
    """Handle /start command"""
    try:
        event_data = load_json_data("schedule.json")
        event_name = event_data.get("event", {}).get("name", settings.FORUM_NAME)
        event_date = event_data.get("event", {}).get("date", "")
        
        welcome_text = (
            f"👋 Добро пожаловать на {event_name}!\n\n"
            f"📅 Дата: {event_date}\n\n"
            "Я помогу вам получить информацию о конференции. "
            "Выберите раздел из меню ниже:"
        )
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=get_main_keyboard()
        )
        
        logger.info(f"User {update.effective_user.id} started the bot")
        
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await update.message.reply_text(
            "Извините, произошла ошибка. Пожалуйста, попробуйте позже."
        )


async def help_command(update: Update, context: CallbackContext):
    """Handle /help command"""
    try:
        help_text = (
            "📚 *Справка по боту*\n\n"
            "*Доступные команды:*\n"
            "/start - Запустить бота и показать меню\n"
            "/schedule - Показать расписание\n"
            "/speakers - Показать список спикеров\n"
            "/faq - Показать часто задаваемые вопросы\n"
            "/venue - Показать информацию о площадке\n"
            "/help - Показать эту справку\n\n"
            "Вы также можете использовать кнопки меню для навигации."
        )
        
        await update.message.reply_text(
            help_text,
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
        
    except Exception as e:
        logger.error(f"Error in help command: {e}")
        await update.message.reply_text("Произошла ошибка при обработке команды.")


async def schedule_command(update: Update, context: CallbackContext):
    """Handle /schedule command - show event schedule"""
    try:
        schedule_data = load_json_data("schedule.json")
        
        if not schedule_data:
            await update.message.reply_text("Не удалось загрузить расписание.")
            return
        
        event_info = schedule_data.get("event", {})
        event_name = event_info.get("name", "")
        event_date = event_info.get("date", "")
        location = event_info.get("location", "")
        stats = event_info.get("stats", {})
        
        # Build schedule text
        text = f"📅 *{event_name}*\n"
        text += f"📆 {event_date}\n"
        text += f"📍 {location}\n\n"
        text += f"📊 Статистика: {stats.get('talks', 0)} докладов, "
        text += f"{stats.get('speakers', 0)} спикеров, "
        text += f"{stats.get('days', 0)} день(дней)\n\n"
        text += "*Расписание:*\n"
        text += "─" * 20 + "\n"
        
        days = schedule_data.get("days", [])
        for day in days:
            day_name = day.get("name", "")
            text += f"\n🗓 *{day_name}*\n"
            
            events = day.get("events", [])
            for event in events:
                time = event.get("time", "")
                title = event.get("title", "")
                event_type = event.get("type", "")
                room = event.get("room", "")
                speaker = event.get("speaker")
                
                # Emoji based on event type
                type_emoji = {
                    "keynote": "🎯",
                    "talk": "💬",
                    "workshop": "🛠",
                    "break": "☕",
                    "discussion": "🤝"
                }.get(event_type, "•")
                
                text += f"{type_emoji} *{time}* - {title}"
                
                if room:
                    text += f" ({room})"
                
                if speaker and speaker.get("name"):
                    text += f"\n   👤 {speaker.get('name')}"
                    if speaker.get("company"):
                        text += f" | {speaker.get('company')}"
                
                text += "\n"
        
        # Add navigation buttons
        keyboard = [
            [
                InlineKeyboardButton("🎤 Спикеры", callback_data="speakers"),
                InlineKeyboardButton("❓ FAQ", callback_data="faq")
            ],
            [
                InlineKeyboardButton("📍 Площадка", callback_data="venue"),
                InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")
            ]
        ]
        
        if update.message:
            await update.message.reply_text(
                text,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif update.callback_query:
            await update.callback_query.message.edit_text(
                text,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
    except Exception as e:
        logger.error(f"Error in schedule command: {e}")
        error_text = "Не удалось загрузить расписание. Попробуйте позже."
        if update.message:
            await update.message.reply_text(error_text)
        elif update.callback_query:
            await update.callback_query.message.edit_text(error_text)


async def speakers_command(update: Update, context: CallbackContext):
    """Handle /speakers command - show list of speakers"""
    try:
        speakers_data = load_json_data("speakers.json")
        
        if not speakers_data:
            await update.message.reply_text("Не удалось загрузить список спикеров.")
            return
        
        text = "🎤 *Спикеры конференции*\n\n"
        
        for i, speaker in enumerate(speakers_data, 1):
            name = speaker.get("name", "")
            company = speaker.get("company", "")
            badge = speaker.get("badge", "")
            topics = speaker.get("topics", [])
            
            text += f"{i}. *{name}*\n"
            
            if badge:
                text += f"   {badge}\n"
            
            if company:
                text += f"   🏢 {company}\n"
            
            if topics:
                text += f"   🏷 {', '.join(topics)}\n"
            
            text += "\n"
        
        keyboard = [
            [
                InlineKeyboardButton("📅 Расписание", callback_data="schedule"),
                InlineKeyboardButton("❓ FAQ", callback_data="faq")
            ],
            [
                InlineKeyboardButton("📍 Площадка", callback_data="venue"),
                InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")
            ]
        ]
        
        if update.message:
            await update.message.reply_text(
                text,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif update.callback_query:
            await update.callback_query.message.edit_text(
                text,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
    except Exception as e:
        logger.error(f"Error in speakers command: {e}")
        error_text = "Не удалось загрузить список спикеров. Попробуйте позже."
        if update.message:
            await update.message.reply_text(error_text)
        elif update.callback_query:
            await update.callback_query.message.edit_text(error_text)


async def faq_command(update: Update, context: CallbackContext):
    """Handle /faq command - show frequently asked questions"""
    try:
        faq_data = load_json_data("faq.json")
        
        if not faq_data:
            await update.message.reply_text("Не удалось загрузить FAQ.")
            return
        
        text = "❓ *Часто задаваемые вопросы*\n\n"
        
        for i, faq in enumerate(faq_data, 1):
            question = faq.get("question", "")
            answer = faq.get("answer", "")
            
            text += f"*{i}. {question}*\n"
            text += f"{answer}\n\n"
        
        keyboard = [
            [
                InlineKeyboardButton("📅 Расписание", callback_data="schedule"),
                InlineKeyboardButton("🎤 Спикеры", callback_data="speakers")
            ],
            [
                InlineKeyboardButton("📍 Площадка", callback_data="venue"),
                InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")
            ]
        ]
        
        if update.message:
            await update.message.reply_text(
                text,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif update.callback_query:
            await update.callback_query.message.edit_text(
                text,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
    except Exception as e:
        logger.error(f"Error in faq command: {e}")
        error_text = "Не удалось загрузить FAQ. Попробуйте позже."
        if update.message:
            await update.message.reply_text(error_text)
        elif update.callback_query:
            await update.callback_query.message.edit_text(error_text)


async def venue_command(update: Update, context: CallbackContext):
    """Handle /venue command - show venue information"""
    try:
        venue_data = load_json_data("venue.json")
        
        if not venue_data:
            await update.message.reply_text("Не удалось загрузить информацию о площадке.")
            return
        
        name = venue_data.get("name", "")
        address = venue_data.get("address", "")
        maps_url = venue_data.get("maps_url", "")
        transport = venue_data.get("transport", [])
        
        text = f"📍 *{name}*\n\n"
        text += f"📌 *Адрес:*\n{address}\n\n"
        text += "*Как добраться:*\n"
        
        for item in transport:
            icon = item.get("icon", "•")
            title = item.get("title", "")
            description = item.get("description", "")
            text += f"{icon} *{title}*: {description}\n"
        
        if maps_url:
            text += f"\n[🗺 Открыть на карте]({maps_url})"
        
        keyboard = [
            [
                InlineKeyboardButton("📅 Расписание", callback_data="schedule"),
                InlineKeyboardButton("🎤 Спикеры", callback_data="speakers")
            ],
            [
                InlineKeyboardButton("❓ FAQ", callback_data="faq"),
                InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")
            ]
        ]
        
        if update.message:
            await update.message.reply_text(
                text,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif update.callback_query:
            await update.callback_query.message.edit_text(
                text,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
    except Exception as e:
        logger.error(f"Error in venue command: {e}")
        error_text = "Не удалось загрузить информацию о площадке. Попробуйте позже."
        if update.message:
            await update.message.reply_text(error_text)
        elif update.callback_query:
            await update.callback_query.message.edit_text(error_text)


async def main_menu_command(update: Update, context: CallbackContext):
    """Show main menu"""
    try:
        event_data = load_json_data("schedule.json")
        event_name = event_data.get("event", {}).get("name", settings.FORUM_NAME)
        event_date = event_data.get("event", {}).get("date", "")
        
        welcome_text = (
            f"👋 Добро пожаловать на {event_name}!\n\n"
            f"📅 Дата: {event_date}\n\n"
            "Выберите раздел из меню ниже:"
        )
        
        if update.callback_query:
            await update.callback_query.message.edit_text(
                welcome_text,
                reply_markup=get_main_keyboard()
            )
        elif update.message:
            await update.message.reply_text(
                welcome_text,
                reply_markup=get_main_keyboard()
            )
        
    except Exception as e:
        logger.error(f"Error in main menu command: {e}")


async def handle_callback(update: Update, context: CallbackContext):
    """Handle inline keyboard button callbacks"""
    try:
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        
        if callback_data == "schedule":
            await schedule_command(update, context)
        elif callback_data == "speakers":
            await speakers_command(update, context)
        elif callback_data == "faq":
            await faq_command(update, context)
        elif callback_data == "venue":
            await venue_command(update, context)
        elif callback_data == "main_menu":
            await main_menu_command(update, context)
        
    except Exception as e:
        logger.error(f"Error in callback handler: {e}")


async def post_init(application: Application):
    """Post initialization callback"""
    logger.info("Bot initialized successfully")
    
    # Get bot info
    bot = application.bot
    bot_info = await bot.get_me()
    logger.info(f"Bot username: @{bot_info.username}")
    logger.info(f"Bot name: {bot_info.name}")


def main():
    """Main entry point"""
    try:
        settings.validate()
        
        application = Application.builder() \
            .token(settings.TELEGRAM_BOT_TOKEN) \
            .post_init(post_init) \
            .build()
        
        # Register command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("schedule", schedule_command))
        application.add_handler(CommandHandler("speakers", speakers_command))
        application.add_handler(CommandHandler("faq", faq_command))
        application.add_handler(CommandHandler("venue", venue_command))
        
        # Register callback query handler
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_callback))
        
        # Register callback query handler for inline buttons
        from telegram.ext import CallbackQueryHandler
        application.add_handler(CallbackQueryHandler(handle_callback))
        
        logger.info("Bot is starting...")
        logger.info(f"Using data from: {DATA_DIR}")
        
        application.run_polling()
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"Error: {e}")
        print("\nPlease create a .env file with required variables.")
        print("Copy .env.example to .env and fill in your bot token.")
        exit(1)
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        exit(1)


if __name__ == "__main__":
    main()
