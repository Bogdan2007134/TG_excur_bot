from config import bot, db
from aiogram import types, Dispatcher
from KeyboardMarkup.KeyboardMarkup import mainMenu
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMedia, Message
from aiogram.utils.callback_data import CallbackData
from lists_dictionaries.city_lists import cities
from .excur import excur_Off_decorator

cities_callback = CallbackData("cities", "page")


def get_cities_keyboard(cities_callback, page: int = 0) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    has_next_page = len(cities) > page + 1

    if page != 0:
        keyboard.insert(
            InlineKeyboardButton(
                text="< Назад",
                callback_data=cities_callback.new(page=page - 1)
            )
        )

    if has_next_page:
        keyboard.insert(
            InlineKeyboardButton(
                text="Вперёд >",
                callback_data=cities_callback.new(page=page + 1)
            )
        )

    if 0 <= page < len(cities):
        pages = cities[page]["display_name"]
        keyboard.insert(
            InlineKeyboardButton(
                text=f"Выбрать {pages}",
                callback_data="cities_c" + str(page + 1)
            )
        )

    return keyboard

@excur_Off_decorator
async def insert_a_city(call: types.CallbackQuery):
    city_data = cities[0]
    caption = f"<b>{city_data.get('display_name')}</b>"
    keyboard = get_cities_keyboard(cities_callback)  # Page: 0
    db.add_page(call.from_user.id, 0)
    await bot.send_photo(
        chat_id=call.from_user.id,
        photo=city_data.get("image_url"),
        caption=caption,
        parse_mode="HTML",
        reply_markup=keyboard
    )

@excur_Off_decorator
async def insert_a_city_back(call: types.CallbackQuery):
    page = int(db.get_page(call.from_user.id))
    city_data = cities[page]
    caption = f"<b>{city_data.get('display_name')}</b>"
    keyboard = get_cities_keyboard(cities_callback, page)  # Page: 0
    
    photo_excurs = InputMedia(type="photo", media=city_data.get("image_url"), parse_mode="HTML", caption=caption)
    await call.message.edit_media(photo_excurs, keyboard)
    

async def city_page_handler(call: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    city_data = cities[page]
    caption = f"<b>{city_data.get('display_name')}      {page + 1}/3</b>"
    keyboard = get_cities_keyboard(cities_callback, page)
    
    db.add_page(call.from_user.id, page)
    photo = InputMedia(type="photo", media=city_data.get("image_url"), caption=caption)
    await call.message.edit_media(photo, keyboard)


def register_handlers_list_cities(dp: Dispatcher):
    dp.register_callback_query_handler(insert_a_city, text='clicksity')
    dp.register_callback_query_handler(insert_a_city_back, text='backclicksity')
    dp.register_callback_query_handler(city_page_handler, cities_callback.filter())
    

    
