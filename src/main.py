import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import os
from dotenv import load_dotenv

load_dotenv()

from src.application.parser_factory import create_malibu_service

BOT_SECRET_KEY = os.getenv("BOT_SECRET_KEY")
bot = telebot.TeleBot(BOT_SECRET_KEY)

service = create_malibu_service()

def create_main_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🚀 Запуск парсинга", callback_data="start_parsing"))
    return markup

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        "🤖 Бот для парсинга готов!\n\nНажмите кнопку ниже:",
        reply_markup=create_main_keyboard()
    )

@bot.callback_query_handler(func=lambda call: call.data == "start_parsing")
def start_parsing(call):
    chat_id = call.message.chat.id
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.message_id,
        text="🔄 Выполняется парсинг... Подождите.",
        reply_markup=None
    )

    try:
        malibu_cinema_id = service.get_malibu_cinema_id()
        service.malibu_movies_record(malibu_cinema_id)

        bot.send_message(chat_id, "✅ Парсинг успешно завершён!")
    except Exception as e:
        logging.exception("Ошибка при парсинге:")
        bot.send_message(chat_id, f"❌ Ошибка при парсинге: {e}")
    finally:
        service.main_parser.driver.quit()
        service.db.close()

        bot.send_message(chat_id, "Хотите выполнить парсинг ещё раз?", reply_markup=create_main_keyboard())

bot.polling()









#-----------------------------------old-------------------------------------------
# import telebot
# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
# from telebot import types
# import subprocess
# import os
# import sys
# import logging

# PARSING_SCRIPT_PATH = 'run_malibu.py'
# ADMIN_ID = ''

# def create_main_keyboard():
#     markup = InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton("🚀 Запуск парсинга", callback_data="start_parsing"))
#     return markup

# @bot.message_handler(commands=['start'])
# def start_command(message):
        
#     bot.send_message(
#         message.chat.id,
#         "🤖 Бот для парсинга готов к работе!\n\n"
#         "Нажмите кнопку ниже для запуска:",
#         reply_markup=create_main_keyboard()
#     )

# @bot.callback_query_handler(func=lambda call: call.data == "start_parsing")
# def start_parsing(call, service_parse):
#     # Обновляем сообщение
#     bot.edit_message_text(
#         chat_id=call.message.chat.id,
#         message_id=call.message.message_id,
#         text="🔄 Выполняется парсинг... Пожалуйста, подождите.",
#         reply_markup=None
#     )
    
#     # Запускаем парсинг
#     perform_parsing_subprocess(call.message.chat.id)

# def perform_parsing_subprocess(chat_id, service):
#     """Запускает парсинг как отдельный процесс"""
#     try:
#         status_message = bot.send_message(chat_id, "🔄 Запускаю процесс парсинга...")
#         service_parse.run() 
#         # Запускаем скрипт парсинга
#         result = subprocess.run(
#             [sys.executable, PARSING_SCRIPT_PATH], # используем текущий интерпретатор Python, команда "запусти Python скрипт run_malibu.py"
#             capture_output=True, # перехватываем всё, что скрипт выводит в консоль
#             text=True, # чтобы получить вывод в виде строки, говорим "работай в папке где лежит main.py"
#             cwd=os.path.dirname(os.path.abspath(__file__))  # говорим "работай в папке где лежит main.py"
#         )
#         # Обрабатываем результат
#         if result.returncode == 0:
#             # Успешное выполнение
#             output = result.stdout.strip() if result.stdout else "Парсинг завершен успешно"
            
#             bot.edit_message_text(
#                 chat_id=chat_id,
#                 message_id=status_message.message_id,
#                 text=f"✅ Парсинг успешно завершен!\n\n{output}"
#             )
#         else:
#             # Ошибка выполнения
#             error_output = result.stderr.strip() if result.stderr else "Неизвестная ошибка"
            
#             bot.edit_message_text(
#                 chat_id=chat_id,
#                 message_id=status_message.message_id,
#                 text=f"❌ Ошибка при парсинге:\n{error_output}"
#             )
        
#         # Предлагаем выполнить еще раз
#         bot.send_message(
#             chat_id,
#             "Хотите выполнить парсинг еще раз?",
#             reply_markup=create_main_keyboard()
#         )
        
#     except Exception as e:
#         error_msg = f"❌ Ошибка при запуске парсинга: {str(e)}"
#         logging.error(error_msg)
        
#         bot.send_message(chat_id, error_msg)
#         bot.send_message(
#             chat_id,
#             "Попробовать еще раз?",
#             reply_markup=create_main_keyboard()
#         )


# #--------------------------------------------------------------------------------------------
# # @bot.message_handler(content_types=['photo'])
# # def het_photo(message):
# #     markup = types.InlineKeyboardMarkup()
# #     markup.add(types.InlineKeyboardButton("Open in browser", url="https://bojack.mult-fan.tv/"))
# #     bot.reply_to(message, 'Какое красивое фото', reply_markup=markup)
# #TODO запускаем парсер по комманде юзера парсь!

# # @bot.message_handler(commands=['site', 'website'])
# # def site(message):
# #     webbrowser.open('https://bojack.mult-fan.tv/')


# # @bot.callback_query_handler(func=lambda call: call.data== 'press_mafuka')
# # def handle_press_mafuka(call):
# #     bot.edit_message_text(
# #         chat_id=call.message.chat.id,
# #         message_id=call.message.message_id,
# #         text="Красаучег !!!"
# # )

# # @bot.message_handler(commands=['start', 'main', 'hello'])
# # def main(message):
# #     markup = InlineKeyboardMarkup()
# #     button = InlineKeyboardButton("Нажми меня", callback_data='press_mafuka')
# #     markup.add(button)
    
# #     bot.send_message(
# #         message.chat.id,
# #         f'Привет, {message.from_user.first_name} {message.from_user.last_name}',
# #         reply_markup=markup
# # )

# # @bot.message_handler(commands=['help'])
# # def main(message):
# #     bot.send_message(message.chat.id, '<b>Help</b> <em><u>information</u></em>', parse_mode='html')

# # @bot.message_handler()
# # def info(message):
# #     if message.text.lower() == 'привет':
# #         bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}')
# #     elif message.text.lower() == 'id':
# #         bot.reply_to(message, f'ID: {message.from_user.id}')
 

# # bot.polling(none_stop=True)


# if __name__ == "__main__":
#     print("Бот запущен...")
#     bot.polling(none_stop=True)

