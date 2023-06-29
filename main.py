from random import randint
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from aiogram.types import InputFile
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from volgograd.data_text import *
from Anti_flood.middlewares import ThrottlingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Config._Config_ import BOT_ON
from TOKEN_BOT.TOKEN import tokens, YOOTOKEN
from db import Database
from BUTTON_ import mainMenu, sub_inline_markup

ball = 1

storage = MemoryStorage()
bot = Bot(token=tokens)
dp = Dispatcher(bot=bot, storage=storage)
word_good = ["Интересно", "Прикольно", "Удивительно"]

db = Database('database.db')

all_users = {}

async def on_startup(message: types.Message):
    print(BOT_ON)
    
# Регистрационный блок
@dp.message_handler(commands=['start'])  # Блок комманд
async def start_func(message: types.Message):
    if(not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, "Укажите ваш ник!")
    else:
        await bot.send_message(message.from_user.id, f'Приветствую тебя повторно {message.chat.first_name} в нашем боте', reply_markup=mainMenu)

@dp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == 'private':
        if message.text == 'ПРОФИЛЬ':
            user_nickname = "Ваш ник:" + db.get_nickname(message.from_user.id)
            await bot.send_message(message.from_user.id, user_nickname)
                
        elif message.text == 'Купить экскурсию':
            await bot.send_message(message.from_user.id, "Покупка экскурсии", reply_markup=sub_inline_markup)
        
        else:
            if db.get_signup(message.from_user.id) == 'setnickname':
                if(len(message.text) > 15):
                    await bot.send_message(message.from_user.id, "Никнейм не должен превышать 15 символов")
                elif '@' in message.text or '/' in message.text:
                    await bot.send_message(message.from_user.id, "Ваш никнейм содержит запрещеный символ!")
                else:
                    db.set_nickname(message.from_user.id, message.text)
                    db.set_signup(message.from_user.id, 'done')
                    await bot.send_message(message.from_user.id, "Регистрация прошла успешно!", reply_markup=mainMenu)
            else:
                await bot.send_message(message.from_user.id, "У вас уже установлен ник!")
                
# Система оплаты
@dp.callback_query_handler(text="submonth")
async def subexcur(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_invoice(chat_id=call.from_user.id, title="Оформление товара", description="Тестовое описание товара", payload="month_sub", provider_token=YOOTOKEN, currency="RUB", start_parameter="test_bot", prices=[{"label": "Руб", "amount": 15000}])

@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == "month_sub":
        operation = '+'
        excur_sub = 1
        db.plus(message.from_user.id, operation, excur_sub)
        await bot.send_message(message.from_user.id, "Вы купили экскурсию!")
        
        
    
    
    
                
# Блок комманд              
@dp.message_handler(commands=['Волгоград'])  
async def volgograd_func(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=len(volgograd_list))
    if all_users[message.chat.id]["direction"] == "":
        buy_button = types.InlineKeyboardButton('Купить_экскурсию')
        
        markup.add(buy_button)
        for i in volgograd_list:
            markup.add(i)
            
        await bot.send_message(message.chat.id, 'Какой сценарий вы хотите выбрать?', reply_markup=markup)
    else:
        markup.add(all_users[message.chat.id]["direction"])
        await bot.send_message(message.chat.id, "Какой именно вы сценарий хотите допройти?", reply_markup=markup)



@dp.message_handler(text=[''])  
async def buy_func(message):
    pass
    # try:
    #     await bot.send_message(message.chat.id, "В будущем тут будет система оплаты но будем\nсчитать что вы уже все оплатили")
    #     all_users[message.chat.id]['condition'] = True
    #     await bot.send_message(message.chat.id, "Оплата успешно прошла")
    # except KeyError as key:
    #     await bot.send_message(message.chat.id, "Извините за неудобства, но начните сначала")
    #     print(f"[ERROR] error in buy_func {key}")
    #     await start_func(message)
    



# Основной алгоритм экскурсий
@dp.message_handler(content_types=['text'])  
async def vol_Scen(message):
    try:

        if message.text == 'Я думаю это первое':
            all_users[message.chat.id]["interactiv_direction"] = 0
        elif message.text == 'Я думаю это второе':
            all_users[message.chat.id]["interactiv_direction"] = 1
        elif message.text == 'Я думаю это третье':
            all_users[message.chat.id]["interactiv_direction"] = 2
            
        if all_users[message.chat.id]['condition'] == True and (message.text == "Военный сюжет" or message.text == "Романтический сюжет" or message.text == "Интерактивный сюжет"):
            all_users[message.chat.id]['progress'] = 0
            all_users[message.chat.id]['direction'] = message.text
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, row_width=1)
            next = types.InlineKeyboardButton(
                word_good[randint(0, len(word_good)-1)])
            markup.add(next)
            await bot.send_message(message.chat.id, "Начнем нашу экскурсию", reply_markup=markup)
        elif all_users[message.chat.id]['condition'] == True and (message.text in word_good or message.text == 'Я думаю это первое' or message.text == 'Я думаю это второе' or message.text == 'Я думаю это третье'):
            all_users[message.chat.id]['progress'] += 1
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, row_width=1)
            next = types.InlineKeyboardButton(
                word_good[randint(0, len(word_good)-1)])
            helping = types.InlineKeyboardButton("/help")
            interactiv_button_0 = types.InlineKeyboardButton("Я думаю это первое")
            interactiv_button_1 = types.InlineKeyboardButton("Я думаю это второе")
            interactiv_button_2 = types.InlineKeyboardButton("Я думаю это третье")

            try:
                if len(volgograd[all_users[message.chat.id]['direction'].replace(" ", "")][all_users[message.chat.id]['progress']][all_users[message.chat.id]['interactiv_direction']][2]) == 4:
                    markup.add(interactiv_button_0, interactiv_button_1, interactiv_button_2, helping)
            except IndexError:
                markup.add(next, helping)
                
            if len(volgograd[all_users[message.chat.id]['direction'].replace(" ", "")][all_users[message.chat.id]['progress']][all_users[message.chat.id]['interactiv_direction']][0]) == 1: 
                await bot.send_message(message.chat.id, volgograd[all_users[message.chat.id]['direction'].replace(" ", "")][all_users[message.chat.id]['progress']][0], reply_markup=markup)
            else:
                await bot.send_message(message.chat.id, volgograd[all_users[message.chat.id]['direction'].replace(" ", "")][all_users[message.chat.id]['progress']][all_users[message.chat.id]['interactiv_direction']], reply_markup=markup)
           
   
            if len(volgograd[all_users[message.chat.id]['direction'].replace(" ", "")][all_users[message.chat.id]['progress']][all_users[message.chat.id]['interactiv_direction']][0]) == 1:
                await bot.send_photo(message.chat.id, open(volgograd[all_users[message.chat.id]['direction'].replace(" ", "")][all_users[message.chat.id]['progress']][1], 'rb'), reply_markup=markup)
            else:
                await bot.send_photo(message.chat.id, open(volgograd[all_users[message.chat.id]['direction'].replace(" ", "")][all_users[message.chat.id]['progress']][all_users[message.chat.id]['interactiv_direction']][0], 'rb'), reply_markup=markup)
        else:
            await bot.send_message(message.chat.id, "Пожалуйста пользуйтесь встроенными командами\n\nИли\n\nСкорее всего вы еще не оплатили экскурсию,\nсамое время это сделать")
            

    except FileNotFoundError:
        pass
    
    except IndexError:
        await bot.send_message(message.chat.id, "Экскурсия закончилась, ждем вас еще")
        all_users[message.chat.id]['condition'] = False
        all_users[message.chat.id]['direction'] = ""
        await start_func(message)
        
        
    except KeyError:
        print(message.chat.id, "неправильно ввел", message.text)
        await bot.send_message(message.chat.id, "Пожалуйста, пользуйтесь командами")

if __name__ == '__main__':
    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)

