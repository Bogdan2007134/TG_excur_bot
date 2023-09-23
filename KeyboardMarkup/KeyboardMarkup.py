from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def mainMenu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='ВЫБРАТЬ ГОРОД', callback_data='clicksity')
            ],
            [
                InlineKeyboardButton(text='Меню', callback_data='backformenu')
            ],
        ],
        resize_keyboard=True 
    )


    return kb

def navigation_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='ВЫБРАТЬ ГОРОД', callback_data='clicksity')
            ],
            [
                InlineKeyboardButton(text='Ввести промокод', callback_data='promocode')
            ],
            [
                InlineKeyboardButton(text='Получить промокод', callback_data='givepromocode')
            ],
            [
                InlineKeyboardButton(text='Гид Паспарту', callback_data='start_gpt')
            ],
            [
                InlineKeyboardButton(text='Написать поддержке', callback_data='send_feedback')
            ],
        ],
        resize_keyboard=True
    )


    return kb

def start_gpt() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Гид Паспарту', callback_data='start_gpt')
            ],
        ],
        resize_keyboard=True
    )


    return kb

def cancel_gpt() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Отключить Гида', callback_data='cancel_gpt')
            ],
        ],
        resize_keyboard=True
    )


    return kb

def back_for_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Меню', callback_data='backformenu')
            ],
        ],
        resize_keyboard=True
    )


    return kb

def admin_panel() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Рассылка', callback_data='rassilka')
            ],
            [
                InlineKeyboardButton(text='Редактор Цен', callback_data='select_price')
            ],
            [
                InlineKeyboardButton(text='Статистика пользователей', callback_data='send_statistics_users')
            ],
            [
                InlineKeyboardButton(text='Статистика экскурсий', callback_data='send_statistics_excursion')
            ],
            [
                InlineKeyboardButton(text='Промокоды', callback_data='admin_promocode')
            ],
            
        ],
        resize_keyboard=True 
    )


    return kb

def clear_reset_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton("Отмена", callback_data='clearreset'),
    )

    return keyboard 

def clear_reset_promo_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Написать поддержке', callback_data='send_feedback')
            ],
            [
                InlineKeyboardButton("Отмена", callback_data='clearreset'),
            ],
        ],
        resize_keyboard=True
    )


    return kb

def promocode_admin() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Добавить промокод', callback_data='insert_promocode')
            ],
            [
                InlineKeyboardButton(text='Удалить промокод', callback_data='delete_promocode')
            ],
        ],
        resize_keyboard=True 
    )


    return kb

