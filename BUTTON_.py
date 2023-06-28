from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btProfile = KeyboardButton('ПРОФИЛЬ')
SITY = KeyboardButton('/Волгоград')

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(btProfile, SITY)