# создание экземпляра бота
import os
from telebot import TeleBot
from dotenv import load_dotenv

load_dotenv()

BOT_SECRET_KEY = os.getenv("BOT_SECRET_KEY")

if not BOT_SECRET_KEY:
    raise RuntimeError("BOT_SECRET_KEY не найден в .env")

bot = TeleBot(BOT_SECRET_KEY, parse_mode="HTML")
