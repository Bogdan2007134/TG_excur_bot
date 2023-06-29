from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

btProfile = KeyboardButton('ПРОФИЛЬ')
shops = KeyboardButton('Купить экскурсию')
SITY = KeyboardButton('/Волгоград')
Reg = KeyboardButton('/Регистрация')


mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(btProfile, SITY, Reg, shops)

sub_inline_markup = InlineKeyboardMarkup(row_width=1)

btnSubMonth = InlineKeyboardButton(text="1 шт. - 9999руб", callback_data="submonth")
sub_inline_markup.insert(btnSubMonth)
