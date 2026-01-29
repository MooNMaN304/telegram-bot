from src.application.bot.bot_factory import bot
from src.application.bot.handlers import register_handlers

from src.utils.logger import setup_logging, get_logger


def run_bot():
    register_handlers(bot)
    bot.infinity_polling()

if __name__ == "__main__":
    setup_logging()

    # Получайте логгер в модулях
    logger = get_logger(__name__)
    logger.info("Стандартная библиотека logging")
    run_bot()
