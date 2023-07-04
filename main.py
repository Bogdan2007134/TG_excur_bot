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
from Markup_Button import mainMenu, sub_inline_markup, Sity
from Delete_Msg.DelMsg import delete_message 

# регистрация бота
storage = MemoryStorage()
bot = Bot(token=tokens)
dp = Dispatcher(bot=bot, storage=storage)

# регистрация БД
db = Database('database.db')

# это мы уберём наверное
all_users = {}
word_good = ["Интересно", "Прикольно", "Удивительно"]

# уведомление о старте бота
async def on_startup(message: types.Message):
    print(BOT_ON)
    
# Регистрационный блок
@dp.message_handler(commands=['start'], commands_prefix = "/!")  # Блок комманд
async def start_func(message: types.Message) -> None:
    if(not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, f'Приветствую тебя {message.chat.first_name} в нашем боте', reply_markup=Reg_menu())
    else:
        await bot.send_message(message.from_user.id, f'Приветствую тебя повторно {message.chat.first_name} в нашем боте', reply_markup=mainMenu())
        await message.delete()   
                
# Система оплаты
@dp.callback_query_handler(text="submonth")
async def subexcur(call: types.CallbackQuery) -> None:
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_invoice(chat_id=call.from_user.id, title="Оформление товара", description="Тестовое описание товара", payload="month_sub", provider_token=YOOTOKEN, currency="RUB", start_parameter="test_bot", prices=[{"label": "Руб", "amount": 15000}])

@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == "month_sub":
        db.plus(message.from_user.id, '+', 1)
        await bot.send_message(message.from_user.id, "Вы купили экскурсию! Вам на счёт начислен 1 балл который вы сможете потратить на экскурсию!")
        
              
# Блоки комманд

@dp.message_handler(text=['🛒КУПИТЬ ЭКСКУРСИЮ🛒'])  
async def buy_excur(message: types.Message) -> None:
    await bot.send_message(message.from_user.id, "Покупка экскурсии", reply_markup=sub_inline_markup)
    await message.delete()

@dp.message_handler(text=['🏘ВЫБРАТЬ ГОРОД🏘'])  
async def sity_set(message: types.Message) -> None:
    await bot.send_message(message.from_user.id, "Выберите город:", reply_markup=Sity())
    await message.delete()
    
@dp.message_handler(text=['🆘ПОМОЩЬ🆘'])  
async def help_sos(message: types.Message) -> None:
    await bot.send_message(message.from_user.id, "/start - перезапук бота")
    await message.delete()
 
@dp.message_handler(text=['💰БАЛАНС💰'])  
async def balance_func(message: types.Message) -> None:        
    user_balance = "Ваш баланс: " + db.get_balance(message.from_user.id) + " баллов\n" + "Что-бы пополнить баллы необходимо нажать на 'КУПИТЬ ЭКСКУРСИЮ'"
    await bot.send_message(message.from_user.id, user_balance)
              
@dp.message_handler(text=['Волгоград'])  # это надо доделать потом с Богданом
async def volgograd_func(message: types.Message) -> None:
    await bot.send_message(message.from_user.id, "*Алгоритм экскурсий ещё не реализован*")
    await message.delete()
    # markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=len(volgograd_list))
    # if all_users[message.chat.id]["direction"] == "":
        
    #     for i in volgograd_list:
    #         markup.add(i)
            
    #     await bot.send_message(message.chat.id, 'Какой сценарий вы хотите выбрать?', reply_markup=markup)
    # else:
    #     markup.add(all_users[message.chat.id]["direction"])
    #     await bot.send_message(message.chat.id, "Какой именно вы сценарий хотите допройти?", reply_markup=markup)  



# Основной алгоритм экскурсий пока не работает
@dp.message_handler(content_types=['text'])  
async def vol_Scen(message: types.Message) -> None:
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

# активация при запуске бота
if __name__ == '__main__':
    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)

