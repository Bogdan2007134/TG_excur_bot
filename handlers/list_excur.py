from config import bot, db, YOOTOKEN
from aiogram import types, Dispatcher
from KeyboardMarkup.KeyboardMarkup import mainMenu
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMedia
from aiogram.utils.callback_data import CallbackData
from aiogram.types.web_app_info import WebAppInfo
from lists_dictionaries.excur_lists import excur_data
from .excur import excur_Off_decorator
import re

async def callback_city(call: CallbackQuery):
    """""""""""""Регистрация переменных"""""""""""""
    calldata = call.data
    photo_cities = None
    photo_excur = None
    text_cities = None
    text_excur = None
    keyboard = None
    options = []
    webAppExcur = None
    buy = None
    
    """""""""""""Обработка города и вывод экскурсий"""""""""""""
    if calldata == 'cities_c1':
        photo_cities = 'https://otdihvrossii.ru/wp-content/uploads/2018/03/25895fd533014e7872a190a4c3f210c1.jpg'
        text_cities = '''*краткое описание к Волгограду*
        
    Выберите экскурсию:'''
        
        options = [
            {
                'text': "Военный Волгоград",
                'callback_data': 'excur_military_volgograd'
            },
            {
                'text': "Интерактивный Волгоград",
                'callback_data': 'excur_interactive_volgograd'
            },
            {
                'text': "Романтический Волгоград",
                'callback_data': 'excur_roman_volgograd'
            },
            {
                'text': "Назад",
                'callback_data': 'backclicksity'
            }
        ]
        
    elif calldata == 'cities_c2':
        photo_cities = 'https://st.avtoturistu.ru/images/f/c/8/1/730/big/0e69f00442.jpg'
        text_cities = '''*краткое описание к Астрахани*
        
    Выберите экскурсию:'''
        
        options = [
            {
                'text': "Историческая Астрахань",
                'callback_data': 'excur_histori_astrakhan'
            },
            {
                'text': "Интерактивная Астрахань",
                'callback_data': 'excur_interactive_astrakhan'
            },
            {
                'text': "Рыбный маршрут Астрахани",
                'callback_data': 'excur_fish_astrakhan'
            },
            {
                'text': "Назад",
                'callback_data': 'backclicksity'
            }
        ]

    elif calldata == 'cities_c3':
        photo_cities = 'https://sportishka.com/uploads/posts/2022-02/1645499321_5-sportishka-com-p-priroda-krima-turizm-krasivo-foto-5.jpg'
        text_cities = '''*краткое описание к Крыму*
        
    Выберите экскурсию:'''
        
        options = [
            {
                'text': "Набережная Ялты, еë секреты и тайны",
                'callback_data': 'excur_yalta0secret_crimea'
            },
            {
                'text': "Интерактивный Крым",
                'callback_data': 'excur_interactive_crimea'
            },
            {
                'text': "Прогулка по старым улочкам Ялты",
                'callback_data': 'excur_street0yalta_crimea'
            },
            {
                'text': "Назад",
                'callback_data': 'backclicksity'
            }
        ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=option['text'], callback_data=option['callback_data'])
            ] for option in options
        ],
        resize_keyboard=True
    )

    if text_cities != None and photo_cities != None and keyboard != None:
        photo_cities_ = InputMedia(type="photo", media=photo_cities, parse_mode="HTML", caption=text_cities)
        await call.message.edit_media(photo_cities_, keyboard)
    
        
    """""""""""""Выбор экскурсии"""""""""""""

    if calldata in excur_data:
        data = excur_data[calldata]
        photo_excur = data['photo_excur']
        text_excur = data['text_excur']
        buy = data['buy']
        webAppExcur = data['webAppExcur']

        keyboard_excur = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Описание', web_app=webAppExcur)
            ],
            [
                InlineKeyboardButton(text='Купить', callback_data='buy_' + buy) 
            ],
            [
                InlineKeyboardButton(text='Ввести промокод', callback_data='promocode')
            ],
            [
                InlineKeyboardButton(text='Отмена', callback_data='backclicksity') 
            ],
        ],
        resize_keyboard=True
    )
    
    if text_excur and photo_excur and keyboard_excur:
        photo_excurs = InputMedia(type="photo", media=photo_excur, parse_mode="HTML", caption=text_excur)
        await call.message.edit_media(photo_excurs, keyboard_excur)
        
     
def register_handlers_list_excur(dp: Dispatcher):
    dp.register_callback_query_handler(callback_city, lambda c: c.data.startswith('cities_') 
                                                                     or c.data.startswith('excur_') and not (c.data.startswith('excur_start') or c.data.startswith('buy_') or c.data.startswith('clearreset') 
                                                                                                             or c.data.startswith('support_') or c.data.startswith('excur_back') or c.data.startswith('score_')))

    