import os
from src.application.bot.bot_factory import bot
from src.application.bot.handlers import register_handlers

from src.utils.logger import setup_logging, get_logger, set_service_context


def run_bot():
    register_handlers(bot)
    bot.infinity_polling()


if __name__ == "__main__":
    service_name = os.getenv("SERVICE_NAME", "telegram-bot")
    server_location = os.getenv("SERVER_LOCATION", "unknown")
    setup_logging(service_name=service_name, server_location=server_location)
    set_service_context(service_name, server_location)

    logger = get_logger(__name__)
    logger.info(f"Starting Telegram Bot on {server_location}...")
    run_bot()
