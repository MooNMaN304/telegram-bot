from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from src.db.movies.movie_model import MovieModel
from src.db.sessions.session_model import SessionModel


def admin_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🚀 Запуск парсинга", callback_data="start_parsing"))
    kb.add(InlineKeyboardButton("🎬 Фильмы на сегодня", callback_data="films_today"))
    return kb


def user_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🎬 Фильмы на сегодня", callback_data="films_today"))
    kb.add(InlineKeyboardButton("🏛 Кинотеатры", callback_data="cinemas_list"))
    return kb


def cinemas_keyboard(cinemas: list):
    kb = InlineKeyboardMarkup()
    for cinema in cinemas:
        kb.add(InlineKeyboardButton(cinema.name, callback_data=f"cinema_info_{cinema.id}"))
    kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main"))
    return kb


def cinema_detail_keyboard(cinema_id: int):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🎬 Фильмы в этом кинотеатре", callback_data=f"cinema_movies_{cinema_id}"))
    kb.add(InlineKeyboardButton("⬅️ К списку кинотеатров", callback_data="cinemas_list"))
    return kb


def film_for_today(films: list):
    kb = InlineKeyboardMarkup()
    for film in films:
        kb.add(InlineKeyboardButton(film.name, callback_data="sessions" + str(film.id)))
    kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main"))
    return kb


def sessions_by_film(sessions: list[SessionModel]):
    kb = InlineKeyboardMarkup()
    for session in sessions:
        time_str = session.date.strftime("%H:%M")
        kb.add(InlineKeyboardButton(text=time_str, callback_data="session" + str(session.id)))
    kb.add(InlineKeyboardButton("⬅️ Назад к фильмам", callback_data="films_today"))
    return kb
