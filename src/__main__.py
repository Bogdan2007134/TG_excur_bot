import os
import sys
import json
import uvicorn
import logging
from print_colorama import error

from config.config import settings, dp, bot
from db.database import async_session_maker

from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, CallbackQuery, Update
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode

from bot.middlewares.db import DataBaseSession

from utils.startup_shutdown import on_startup, on_shutdown

from bot.client.handlers import router as client_router

from api.client.routers import router as api_router

routers_fa = [api_router]

routers_ag = [client_router]

app = FastAPI(
    title="BruttoStore App", on_startup=[on_startup], on_shutdown=[on_shutdown]
)
templates = Jinja2Templates(directory=r".\web\templates")
app.mount("/static", StaticFiles(directory=rf"{settings.STATIC_FOLDER}"), name="static")

def register_routers_fastApi(app: FastAPI) -> None:
    for router in routers_fa:
        app.include_router(router)


def register_routers_aiogram(dp: Dispatcher) -> None:
    for router in routers_ag:
        dp.include_router(router)


# middelewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["*"],
)

# Register routers
register_routers_aiogram(dp)
register_routers_fastApi(app)

dp.update.middleware(DataBaseSession(session_pool=async_session_maker))

# default
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
    except ValueError:
        print("Invalid request body")
        raise HTTPException(status_code=400, detail="Invalid request body")

    update = Update.model_validate(data, context={"bot": bot})

    await dp.feed_update(bot, update)


# Error handling
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    error(f"ERROR! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    error(f"ERROR! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        logging.getLogger("fastapi").setLevel(logging.DEBUG)
        uvicorn.run(
            app, host=settings.SERVER_HOST, port=settings.SERVER_PORT, workers=True
        )
    except Exception as e:
        logging.error(f"App crashed with error: {e}")
