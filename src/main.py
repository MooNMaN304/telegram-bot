import os
import threading

from prometheus_client import start_http_server

from src.application.bot.bot_factory import bot
from src.application.bot.handlers import register_handlers

from src.utils.logger import setup_logging, get_logger, set_service_context
from src.utils.metrics import service_info

METRICS_PORT = int(os.getenv("METRICS_PORT", "8000"))


def run_bot():
    register_handlers(bot)
    bot.infinity_polling()


def start_metrics_server():
    """Запускает HTTP-сервер с метриками Prometheus в фоновом потоке."""
    try:
        start_http_server(METRICS_PORT)
        logger = get_logger(__name__)
        logger.info("Prometheus metrics server started on port %d", METRICS_PORT)
    except Exception as e:
        logger = get_logger(__name__)
        logger.error("Failed to start metrics server on port %d: %s", METRICS_PORT, e)


if __name__ == "__main__":
    service_name = os.getenv("SERVICE_NAME", "telegram-bot")
    server_location = os.getenv("SERVER_LOCATION", "unknown")
    setup_logging(service_name=service_name, server_location=server_location)
    set_service_context(service_name, server_location)

    logger = get_logger(__name__)

    # Статическая информация о сервисе для Prometheus
    service_info.info({
        "service": service_name,
        "server": server_location,
    })

    # Запускаем metrics HTTP server в фоне
    metrics_thread = threading.Thread(target=start_metrics_server, daemon=True)
    metrics_thread.start()

    logger.info("Starting Telegram Bot on %s (metrics on :%d)...", server_location, METRICS_PORT)
    run_bot()
