from aiogram import executor, types, Dispatcher
from config import dp, db
from loguru import logger
from Anti_flood.middlewares import ThrottlingMiddleware
import json
import os

"""Созданик пустого словаря пользователей"""
users = {}

"""Проверка существует ли users.json"""
if os.path.exists("users.json"):
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)

"""Сохранение данных из словаря users в файл users.json"""


async def dump_users(users):
    if os.path.exists("users.json"):
        with open("users.json", "w", encoding="utf-8") as f:
            json.dump(users, f)

        f.close()


"""Функция при запуске"""


async def on_startup(dp: Dispatcher):
    print("Бот был успешно запущен")
    await dp.bot.set_my_commands(
        [
            types.BotCommand(command="/start", description="Перезапуск бота;"),
            types.BotCommand(command="/menu", description="Открыть меню;"),
        ],
        types.BotCommandScopeAllPrivateChats(),
    )
    logger.success(f"Бот запущен как @{(await dp.bot.get_me()).username}!")


"""Функция при выключении"""


async def on_shutdown(dp: Dispatcher):
    await dump_users(users)
    await dp.storage.close()
    await dp.storage.wait_closed()
    db.close()


"""Регистрация хэндлеров"""
from handlers import (
    client,
    list_cities,
    list_excur,
    excur,
    payment,
    guide_gpt,
    admin,
    filter,
)

list_cities.register_handlers_list_cities(dp)
client.register_handlers_client(dp)
list_excur.register_handlers_list_excur(dp)
excur.register_handlers_excur(dp)
payment.register_payment_handlers(dp)
guide_gpt.register_handlers_guide_gpt(dp)
admin.register_handlers_admins(dp)
filter.register_handlers_filter(dp)


"""Параметры при запуске"""
if __name__ == "__main__":
    db.create_tables()
    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(
        dispatcher=dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown
    )
