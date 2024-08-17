from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo

from config.config import settings

from config import settings

def main_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="ВЫБРАТЬ ГОРОД", web_app=WebAppInfo(url=settings.APP_URL)
    )  # Ссылка на сайт

    builder.adjust(1)
    return builder.as_markup()

def start_excur_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Начать", callback_data="start_excur"
    )

    builder.adjust(1)
    return builder.as_markup()


def next_slide_kb(text) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=text, callback_data="next_slide")

    builder.adjust(1)
    return builder.as_markup()


def interactive_slide_kb(shuffled_list1, shuffled_list2) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    builder.button(text=shuffled_list1[0], callback_data=shuffled_list2[0])

    builder.button(text=shuffled_list1[1], callback_data=shuffled_list2[1])

    builder.button(text=shuffled_list1[2], callback_data=shuffled_list2[2])
    builder.adjust(1)
    return builder.as_markup()
