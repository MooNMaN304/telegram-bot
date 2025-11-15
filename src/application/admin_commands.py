from src.application.value import create_malibu_service


def start_malibu_parsing(chat_id, service: create_malibu_service):
    bot.send_message(chat_id, "🔄 Выполняется парсинг... Пожалуйста, подождите.")
    create_malibu_service()
    bot.send_message(chat_id, "✅ Парсинг завершён успешно!")