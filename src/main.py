from src.application.bot.bot_factory import bot
from src.application.bot.handlers import register_handlers
#from src.db.init_db import init_db

from src.utils.logger import setup_logging, get_logger


def run_bot():
    register_handlers(bot)
    bot.infinity_polling()


if __name__ == "__main__":
    setup_logging()

    # Получайте логгер в модулях
    logger = get_logger(__name__)
    #init_db() #удаляем инициализацию БД, так как она уже выполняется в alembic/env.py
    logger.info("Starting Telegram Bot...")
    run_bot()
