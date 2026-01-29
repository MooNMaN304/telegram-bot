# создание экземпляра бота
import os
from telebot import TeleBot
import telebot
from dotenv import load_dotenv
import logging
from src.utils.logger import UnicodeDecodeHandler

load_dotenv()

BOT_SECRET_KEY = os.getenv("BOT_SECRET_KEY")

if not BOT_SECRET_KEY:
    raise RuntimeError("BOT_SECRET_KEY не найден в .env")

bot = TeleBot(BOT_SECRET_KEY, parse_mode="HTML")
telebot.logger.setLevel(logging.DEBUG)
# telebot.logger.addHandler()
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Wrap it with Unicode decoder
unicode_handler = UnicodeDecodeHandler(console_handler)
unicode_handler.setLevel(logging.DEBUG)
telebot.logger.addHandler(unicode_handler)

