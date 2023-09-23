from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from database.db import Database
import os

load_dotenv()
storage = MemoryStorage()
bot = Bot(os.getenv("TOKEN"), parse_mode="HTML")
dp = Dispatcher(bot=bot, storage=storage)
db = Database("database.db")
YOOTOKEN = os.getenv("YOOTOKENS")
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
NAME_BOT = os.getenv("NAME_BOT")
ADMINS = [1337634166, 5434270608, 324339652]  # 1337634166, 5434270608, 324339652
STANDARD_PRICE = os.getenv("STANDARD_PRICE") # стандартное значение цены экскурсий в копейках для создания бд 