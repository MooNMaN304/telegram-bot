from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from src.movies.movie_model import MovieModel
from src.sessions.session_model import SessionModel

def admin_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🚀 Запуск парсинга", callback_data="start_parsing"))
    kb.add(InlineKeyboardButton("🎬 Фильмы на сегодня", callback_data="films_today"))
    return kb

def user_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🎬 Фильмы на сегодня", callback_data="films_today"))
    return kb


def film_for_today(films: list):
    kb = InlineKeyboardMarkup()
    for film in films:
        kb.add(InlineKeyboardButton(film.name, callback_data="sessions"+ str(film.id)))
    return kb


def sessions_by_film(sessions: list[SessionModel]):
    kb = InlineKeyboardMarkup()
    for session in sessions:
        time_str = session.date.strftime("%H:%M")  # или "%d.%m %H:%M"
        kb.add(
            InlineKeyboardButton(
                text=time_str,
                callback_data="session" + str(session.id)
            )
        )
    return kb