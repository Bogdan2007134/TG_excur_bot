from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def mainMenu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup([
        [KeyboardButton(text='🆘ПОМОЩЬ🆘'), KeyboardButton(text='💰БАЛАНС💰')],
        [KeyboardButton(text='🛒КУПИТЬ ЭКСКУРСИЮ🛒'), KeyboardButton(text='🏘ВЫБРАТЬ ГОРОД🏘')],
    ],
        resize_keyboard=True,
        input_field_placeholder="Выберите"
    )

    return kb

def Sity() -> ReplyKeyboardMarkup:
    kb1 = ReplyKeyboardMarkup([
        [KeyboardButton(text='Волгоград'), KeyboardButton(text='-')],
        [KeyboardButton(text='-'), KeyboardButton(text='-')],
    ],
        resize_keyboard=True,
        input_field_placeholder="Выберите"
    )

    return kb1





sub_inline_markup = InlineKeyboardMarkup(row_width=1)

btnSubMonth = InlineKeyboardButton(text="1 шт. - 500руб", callback_data="submonth")
sub_inline_markup.insert(btnSubMonth)
