import logging
from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from datetime import datetime
from datetime import date

from src.settings import settings
from src.application.bot.keyboards import (
    admin_keyboard,
    user_keyboard,
    film_for_today,
    sessions_by_film,
    cinemas_keyboard,
    cinema_detail_keyboard,
)
from src.application.admin_commands import run_parsing
from src.application.value import get_malibu_controller
from src.application.value import get_user_service, get_movie_service, get_cinema_repository
from src.utils.logger import get_logger
from src.utils.metrics import bot_requests, bot_errors

logger = get_logger(__name__)


def register_handlers(bot: TeleBot):
    # ---------------------------
    #  /start
    # ---------------------------
    @bot.message_handler(commands=["start"])
    def start(message: Message):
        bot_requests.labels(handler="start").inc()
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

        bot.send_message(message.chat.id, text, reply_markup=kb)

    # ---------------------------
    #  Админ → запуск парсинга
    # ---------------------------
    @bot.callback_query_handler(func=lambda call: call.data == "start_parsing")
    def start_parsing(call: CallbackQuery):
        bot_requests.labels(handler="start_parsing").inc()
        chat_id = call.message.chat.id
        user_id = str(call.from_user.id)

        # защита от обычных юзеров
        if user_id != settings.ADMIN_TELEGRAM_ID:
            bot.answer_callback_query(call.id, "❌ У вас нет доступа")
            return

        bot.send_message(chat_id, "🔄 Выполняется парсинг...")

        try:
            msg = run_parsing()
            bot.send_message(chat_id, f"✅ {msg}")
        except Exception as e:
            bot_errors.labels(error_type="parsing").inc()
            logger.exception("Ошибка при выполнении парсинга")
            bot.send_message(chat_id, f"❌ Ошибка: {e}")

    # ---------------------------
    #  Кнопка: фильмы сегодня
    # ---------------------------
    @bot.callback_query_handler(func=lambda call: call.data == "films_today")
    def films_today(call: CallbackQuery):
        bot_requests.labels(handler="films_today").inc()
        chat_id = call.message.chat.id
        try:
            movie_service = get_movie_service()
            movies = movie_service.get_movies_with_sessions_today()

            if not movies:
                bot.send_message(chat_id, "Сегодня нет фильмов.")
                return

            text = "🎬 Фильмы с сеансами сегодня:\n\n"
            bot.send_message(call.message.chat.id, text, reply_markup=film_for_today(movies))
        except Exception as e:
            bot_errors.labels(error_type="films_today").inc()
            logger.exception(f"Ошибка при получении фильмов на сегодня: {e}")
            bot.send_message(chat_id, f"❌ Ошибка: {e}")

    @bot.callback_query_handler(func=lambda call: call.data[:8] == "sessions")
    def get_sessions_by_film(call: CallbackQuery):
        bot_requests.labels(handler="sessions_by_film").inc()
        chat_id = call.message.chat.id
        try:
            movie_service = get_movie_service()
            sessions = movie_service.get_sessions_for_movie_today(
                int(call.data[8:])
            )

            if not sessions:
                bot.send_message(chat_id, "Сегодня нет показов.")
                return

            text = "🎬 Cеансы на сегодня:\n\n"
            bot.send_message(call.message.chat.id, text, reply_markup=sessions_by_film(sessions))
        except Exception as e:
            bot_errors.labels(error_type="sessions_by_film").inc()
            logger.exception(f"Ошибка при получении сеансов: {e}")
            bot.send_message(chat_id, f"❌ Ошибка: {e}")

    # ---------------------------
    #  Кнопка: список кинотеатров
    # ---------------------------
    @bot.callback_query_handler(func=lambda call: call.data == "cinemas_list")
    def cinemas_list(call: CallbackQuery):
        bot_requests.labels(handler="cinemas_list").inc()
        chat_id = call.message.chat.id
        try:
            cinema_repo = get_cinema_repository()
            cinemas = cinema_repo.get_all()

            if not cinemas:
                bot.send_message(chat_id, "Кинотеатры не найдены.")
                return

            bot.edit_message_text(
                chat_id=chat_id,
                message_id=call.message.message_id,
                text="🏛 Выберите кинотеатр:",
                reply_markup=cinemas_keyboard(cinemas)
            )
        except Exception as e:
            bot_errors.labels(error_type="cinemas_list").inc()
            logger.exception(f"Ошибка при получении списка кинотеатров: {e}")
            bot.answer_callback_query(call.id, f"❌ Ошибка: {e}")

    # ---------------------------
    #  Кнопка: инфо о кинотеатре
    # ---------------------------
    @bot.callback_query_handler(func=lambda call: call.data.startswith("cinema_info_"))
    def cinema_info(call: CallbackQuery):
        bot_requests.labels(handler="cinema_info").inc()
        chat_id = call.message.chat.id
        try:
            cinema_id = int(call.data.replace("cinema_info_", ""))
            cinema_repo = get_cinema_repository()
            cinema = cinema_repo.get_by_id(cinema_id)

            if not cinema:
                bot.answer_callback_query(call.id, "❌ Кинотеатр не найден")
                return

            text = f"🏛 *{cinema.name}*\n📍 Адрес: {cinema.address or 'не указан'}"
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=call.message.message_id,
                text=text,
                parse_mode="Markdown",
                reply_markup=cinema_detail_keyboard(cinema_id)
            )
        except Exception as e:
            bot_errors.labels(error_type="cinema_info").inc()
            logger.exception(f"Ошибка при получении информации о кинотеатре: {e}")
            bot.answer_callback_query(call.id, f"❌ Ошибка: {e}")

    # ---------------------------
    #  Кнопка: фильмы в кинотеатре
    # ---------------------------
    @bot.callback_query_handler(func=lambda call: call.data.startswith("cinema_movies_"))
    def cinema_movies(call: CallbackQuery):
        bot_requests.labels(handler="cinema_movies").inc()
        chat_id = call.message.chat.id
        try:
            cinema_id = int(call.data.replace("cinema_movies_", ""))
            movie_service = get_movie_service()
            movies = movie_service.get_movies_by_cinema_today(cinema_id)

            if not movies:
                bot.answer_callback_query(call.id, "В этом кинотеатре сейчас нет фильмов.")
                return

            text = "🎬 Фильмы в выбранном кинотеатре:"
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=call.message.message_id,
                text=text,
                reply_markup=film_for_today(movies)
            )
        except Exception as e:
            bot_errors.labels(error_type="cinema_movies").inc()
            logger.exception(f"Ошибка при получении фильмов в кинотеатре: {e}")
            bot.answer_callback_query(call.id, f"❌ Ошибка: {e}")

    # ---------------------------
    #  Кнопка: назад в главное меню
    # ---------------------------
    @bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
    def back_to_main(call: CallbackQuery):
        bot_requests.labels(handler="back_to_main").inc()
        try:
            user_id = str(call.from_user.id)
            if user_id == settings.ADMIN_TELEGRAM_ID:
                kb = admin_keyboard()
                text = "👑 Привет, админ!\nВыберите действие:"
            else:
                kb = user_keyboard()
                text = "🤖 Бот готов к работе!\nЧто хотите сделать?"

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text,
                reply_markup=kb
            )
        except Exception as e:
            bot_errors.labels(error_type="back_to_main").inc()
            logger.exception(f"Ошибка при возврате в главное меню: {e}")
            bot.answer_callback_query(call.id, f"❌ Ошибка: {e}")
