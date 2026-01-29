import logging
from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from datetime import datetime
from datetime import date

from src.settings import settings
from src.application.bot.keyboards import admin_keyboard, user_keyboard, film_for_today, sessions_by_film
from src.application.admin_commands import run_parsing
from src.application.value import get_malibu_service
from src.application.value import get_user_service, get_movie_repository


def register_handlers(bot: TeleBot):
    # ---------------------------
    #  /start
    # ---------------------------
    @bot.message_handler(commands=["start"])
    def start(message: Message):
        user_service = get_user_service()
        user_service.create_or_update_user(message.from_user)

        user_id = str(message.from_user.id)

        # определение админа
        if user_id == settings.ADMIN_TELEGRAM_ID:
            kb = admin_keyboard()
            text = "👑 Привет, админ!\nВыберите действие:"
        else:
            kb = user_keyboard()
            text = "🤖 Бот готов к работе!\nЧто хотите сделать?"

        bot.send_message(
            message.chat.id,
            text,
            reply_markup=kb
        )

    # ---------------------------
    #  Админ → запуск парсинга
    # ---------------------------
    @bot.callback_query_handler(func=lambda call: call.data == "start_parsing")
    def start_parsing(call: CallbackQuery):
        chat_id = call.message.chat.id
        user_id = str(call.from_user.id)

        # защита от обычных юзеров
        if user_id != settings.ADMIN_TELEGRAM_ID:
            bot.answer_callback_query(call.id, "❌ У вас нет доступа")
            return

        bot.send_message(chat_id, "🔄 Выполняется парсинг...")

        try:
            service = get_malibu_service()
            msg = run_parsing(service)
            bot.send_message(chat_id, f"✅ {msg}")
        except Exception as e:
            logging.exception("Ошибка при выполнении парсинга")
            bot.send_message(chat_id, f"❌ Ошибка: {e}")

    # ---------------------------
    #  Кнопка: фильмы сегодня
    # ---------------------------
    @bot.callback_query_handler(func=lambda call: call.data == "films_today")
    def films_today(call: CallbackQuery):
        chat_id = call.message.chat.id

        movie_repo = get_movie_repository()
        movies = movie_repo.get_movies_with_sessions_today()

        if not movies:
            bot.send_message(chat_id, "Сегодня нет фильмов.")
            return

        text = "🎬 Фильмы с сеансами сегодня:\n\n"
        
        bot.send_message(
            call.message.chat.id,
            text,
            reply_markup=film_for_today(movies)
        )
        
    @bot.callback_query_handler(func=lambda call: call.data[:8] == "sessions")
    def get_sessions_by_film(call: CallbackQuery):
        chat_id = call.message.chat.id

        movie_repo = get_movie_repository()
        sessions = movie_repo.get_sessions_by_movie_and_date(int(call.data[8:]), session_date=date.today())

        if not sessions:
            bot.send_message(chat_id, "Сегодня нет показов.")
            return

        text = "🎬 Cеансы на сегодня:\n\n"
        
        bot.send_message(
            call.message.chat.id,
            text,
            reply_markup=sessions_by_film(sessions)
        )
        
    # @bot.callback_query_handler(func=lambda call: call.data[8:] == "sessions")
    # def get(call: CallbackQuery):
    #     chat_id = call.message.chat.id

    #     movie_repo = get_movie_repository()
    #     movies = movie_repo.get_movies_with_sessions_today()

    #     if not movies:
    #         bot.send_message(chat_id, "Сегодня нет фильмов.")
    #         return

    #     text = "🎬 Фильмы с сеансами сегодня:\n\n"
        
    #     bot.send_message(
    #         call.message.chat.id,
    #         text,
    #         reply_markup=film_for_today(movies)
    #     )



#TODO сделать работающие клавиатуры