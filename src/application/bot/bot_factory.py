# создание экземпляра бота
import os
from telebot import TeleBot
import telebot
from dotenv import load_dotenv
import logging

load_dotenv()

BOT_SECRET_KEY = os.getenv("BOT_SECRET_KEY")

if not BOT_SECRET_KEY:
    raise RuntimeError("BOT_SECRET_KEY не найден в .env")

bot = TeleBot(BOT_SECRET_KEY, parse_mode="HTML")

# Отключаем логирование TeleBot (используем только root logger)
telebot.logger.setLevel(logging.CRITICAL)
telebot.logger.propagate = False

# Очищаем все обработчики TeleBot, чтобы избежать дублирования
for handler in telebot.logger.handlers[:]:
    telebot.logger.removeHandler(handler)
