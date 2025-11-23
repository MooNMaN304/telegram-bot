import logging
from telebot import TeleBot

from src.application.bot.keyboards import admin_keyboard
from src.application.admin_commands import run_parsing
from src.application.value import get_malibu_service
from src.application.value import get_user_service


def register_handlers(bot: TeleBot):
    @bot.message_handler(commands=["start"])
    def start(message):
        # на этом уровне вызвать репозиторий user и записать юзера
        # проверить на админа
        user_service = get_user_service()
        user_service.create_or_update_user(message.from_user)
        bot.send_message(
            message.chat.id,
            "🤖 Бот готов к работе!\n\nВыберите действие:",
            reply_markup=admin_keyboard(),
        )
        
    # админ сервис
    @bot.callback_query_handler(func=lambda call: call.data == "start_parsing")
    def start_parsing(call):
        "handle admin keybord button push start parsing"
        chat_id = call.message.chat.id

        # Вместо редактирования старого сообщения — просто отправляем новое
        bot.send_message(chat_id, "🔄 Выполняется парсинг...")

        try:
            # создаём сервис **только при старте парсинга**
            service = get_malibu_service()
            msg = run_parsing(service)
            bot.send_message(chat_id, f"✅ {msg}")

        except Exception as e:
            logging.exception("Ошибка при выполнении парсинга")
            bot.send_message(chat_id, f"❌ Ошибка: {e}")


    # интерфейс юзера


# """
# Меню 1
# -> Фильмы на сегодня
# -> Фильмы по дате
# Ответ
# -> Список фильмов на сегодня кнопками
# Ответ
# -> Фильм с картинкой, сеансы в кинотеатрах
# """