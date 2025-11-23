# кнопки и клавиатуры
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🚀 Запуск парсинга", callback_data="start_parsing")
    )
    return markup
