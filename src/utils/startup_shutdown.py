import os
import logging
from config.config import settings, dp, bot

from aiogram.types import BotCommand, BotCommandScopeDefault

from db.database import create_db, drop_db


async def on_startup() -> None:
    logging.info("App has been started")
    
    await create_db()

    if not os.path.exists("web/static"):
        os.makedirs("web/static")

    await bot.delete_webhook(True)
    await bot.delete_my_commands(BotCommandScopeDefault())
    
    await bot.set_webhook(
        url=f"{settings.APP_URL}/webhook",
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )
    commands = [
        BotCommand(command="start", description="Перезапуск бота;"),
        BotCommand(command="menu", description="Открыть меню;"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

    logging.info(f"The bot is launched as @{(await bot.get_me()).username}!")
    logging.info("Webhook has been set up")


async def on_shutdown() -> None:
    logging.info("App is shutting down")

