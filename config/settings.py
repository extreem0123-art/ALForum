import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    WEBAPP_URL = os.getenv("WEBAPP_URL", "https://your-domain.com")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    @classmethod
    def validate(cls):
        """Validate required environment variables"""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
        if not cls.WEBAPP_URL:
            raise ValueError("WEBAPP_URL environment variable is required")