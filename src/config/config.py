import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from pydantic import SecretStr, validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any, List

load_dotenv(override=True)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, env_file_encoding="utf-8"
    )

    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 8000

    APP_URL: str = ""        
    STATIC_FOLDER: str = "web/static"

    DB_NAME: str = "database.db"

    TOKEN_BOT: SecretStr = ""
    BOT_NAME: str = ""
    ADMIN_ID: list

    HELLO_PATH: str = "resources\\maintxt\\hello.txt"
    ADMIN_HELLO_PATH: str = "resources\\maintxt\\admin_hello.txt"

    MAIN_PHOTOS: str = "resources\\photos\\main_photo.jng"
    
    


settings = Settings()

bot = Bot(
    settings.TOKEN_BOT.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()
