from random import randint
from Delete_Msg.DelMsg import delete_message
from Anti_flood.middlewares import ThrottlingMiddleware
from Markup_Button import mainMenu, sub_inline_markup, Sity, back_inline_markup

from aiogram.types import InputFile
from aiogram.types.message import ContentType
from aiogram.dispatcher.filters import Command
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db import Database
from Config._Config_ import BOT_ON
from TOKEN_BOT.TOKEN import tokens, YOOTOKEN

from city.krim.data_text import krim_list
from city.astrahan.data_text import astrahan_list
from city.volgograd.data_text import volgograd_list

return_list = []
all_list = [volgograd_list, krim_list, astrahan_list]

for index in all_list:
    for j in index:
        return_list.append(j)
print(return_list)

storage = MemoryStorage()
bot = Bot(token=tokens)
dp = Dispatcher(bot=bot, storage=storage)

word_good = ["Интересно", "Прикольно", "Удивительно"]

db = Database('database.db')


async def on_startup(message: types.Message):
    print(BOT_ON)
    
# Регистрационный блок
@dp.message_handler(commands=['start'])  # Блок комманд
async def start_func(message: types.Message) -> None:
    if(not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, f'Приветствую тебя {message.chat.first_name} в нашем боте', reply_markup=mainMenu())
    else:
        await bot.send_message(message.from_user.id, f'Приветствую тебя повторно {message.chat.first_name} в нашем боте', reply_markup=mainMenu())
 
# Система оплаты:
@dp.callback_query_handler(text="subexcur")
async def subexcur(call: types.CallbackQuery) -> None:
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_invoice(chat_id=call.from_user.id, title="Оформление товара", description="Тестовое описание товара", payload="excur_sub", provider_token=YOOTOKEN, currency="RUB", start_parameter="test_bot", prices=[{"label": "Руб", "amount": 15000}])

# проверка оплатил ли пользователь ипотеку
@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    
# вывод и действия после оплаты
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == "excur_sub":
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
    await bot.send_message(message.from_user.id, "Назад", reply_markup=back_inline_markup)
    await message.delete()
    
@dp.message_handler(text=['🆘ПОМОЩЬ🆘'])  
async def help_sos(message: types.Message) -> None:
    await bot.send_message(message.from_user.id, "/start - перезапук бота")
    await message.delete()
 
@dp.message_handler(text=['💰БАЛАНС💰'])  
async def balance_func(message: types.Message) -> None:        
    user_balance = "Ваш баланс: " + db.get_balance(message.from_user.id) + " баллов\n" + "Что-бы пополнить баллы необходимо нажать на 'КУПИТЬ ЭКСКУРСИЮ'"
    await bot.send_message(message.from_user.id, user_balance)

@dp.callback_query_handler(lambda query: query.data == 'backs')
async def inline_button_callback(query: types.CallbackQuery):
    await query.message.edit_text("Вы вернулись назад!", reply_markup=mainMenu())
    
              
"""
тут первая комментированная строчка в трех последующих функций
моих, потом раскомментится когда база данных будет работать, она
работает с выбранным городом и ID пользователя
"""
@dp.message_handler(text=['Волгоград'])
async def volgograd_func(message: types.Message) -> None:
    db.change_city(message.from_user.id, 'Волгоград')
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=len(volgograd_list))
        
    for i in volgograd_list:
        markup.add(i)
            
    await bot.send_message(message.chat.id, 'Какой сценарий вы хотите выбрать?', reply_markup=markup)
    
    
@dp.message_handler(text=['Крым'])
async def krim_func(message: types.Message) -> None:
    db.change_city(message.from_user.id, 'Крым')
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=len(krim_list))
        
    for i in krim_list:
        markup.add(i)
            
    await bot.send_message(message.chat.id, 'Какой сценарий вы хотите выбрать?', reply_markup=markup)
    
@dp.message_handler(text=['Астрахань'])
async def astrahan_func(message: types.Message) -> None:
    db.change_city(message.from_user.id, 'Астрахань')
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=len(astrahan_list))
        
    for i in astrahan_list:
        markup.add(i)
            
    await bot.send_message(message.chat.id, 'Какой сценарий вы хотите выбрать?', reply_markup=markup)
    
@dp.message_handler(text=[x for x in return_list])
async def volgograd_func(message: types.Message) -> None:
    print(message.text + "234234")

    """
    тут у нас будет список экскурсий и сразу же описание к ним и покупка
    ебой оно внатуер работает :))))))))))
    """
    
    

# Основной алгоритм экскурсий пока не работает
@dp.message_handler(content_types=['text'])  
async def vol_Scen(message: types.Message) -> None:
     
    try:
        """
        все ниже перечисленные параметры это всего лишь
        запросы из базы данных
         
        весь алгоритм переделан так:
        
        city_for_user - это у нас выбор города юзера
        direction_for_user - это направление экскурсии в городе
        progression_for_user - прогресс по экскурсии
        interactiv_direction_for_user - интерактивное направление если таковое имеется
        
        # reset_progression_for_user - сброс прогреса
        # change_direction_for_user - выбор направления
        # update_progression_for_user - += к прогресу
        # change_interactiv_direction_for_user - выбор интерактивного направления
        """
        city_for_user = db.select_city(message.from_user.id)
        direction_for_user = db.select_direction(message.from_user.id)
        progression_for_user = db.select_progress(message.from_user.id)
        interactiv_direction_for_user = db.select_interactive_direction(message.from_user.id)
        
        # reset_progression_for_user = db.reset_progress(message.from_user.id)
        # change_direction_for_user = db.change_direction(message.from_user.id, message.text)
        # update_progression_for_user = db.update_progress(message.from_user.id)
        # change_interactiv_direction_for_user = db.change_interactiv_direction(message.from_user.id, "число которое потом используется")
        
        if message.text == 'Я думаю это первое':
            db.change_interactiv_direction(message.from_user.id, 0)
        elif message.text == 'Я думаю это второе':
            db.change_interactiv_direction(message.from_user.id, 1)
        elif message.text == 'Я думаю это третье':
            db.change_interactiv_direction(message.from_user.id, 2)
            
        if db.get_balance(message.from_user.id) != 0 and (message.text == "Военный сюжет" or message.text == "Романтический сюжет" or message.text == "Интерактивный сюжет"):
            db.reset_progress(message.from_user.id)
            db.MINUS(message.from_user.id)
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, row_width=1)
            next = types.InlineKeyboardButton(
                word_good[randint(0, len(word_good)-1)])
            markup.add(next)
            await bot.send_message(message.chat.id, "Начнем нашу экскурсию", reply_markup=markup)
        elif all_users[message.chat.id]['condition'] == True and (message.text in word_good or message.text == 'Я думаю это первое' or message.text == 'Я думаю это второе' or message.text == 'Я думаю это третье'):
            db.update_progress(message.from_user.id)
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, row_width=1)
            next = types.InlineKeyboardButton(
                word_good[randint(0, len(word_good)-1)])
            helping = types.InlineKeyboardButton("/help")
            interactiv_button_0 = types.InlineKeyboardButton("Я думаю это первое")
            interactiv_button_1 = types.InlineKeyboardButton("Я думаю это второе")
            interactiv_button_2 = types.InlineKeyboardButton("Я думаю это третье")

            try:
                if len(city_for_user[direction_for_user.replace(" ", "")][progression_for_user][interactiv_direction_for_user][2]) == 4:
                    markup.add(interactiv_button_0, interactiv_button_1, interactiv_button_2, helping)
            except IndexError:
                markup.add(next, helping)
                
            if len(city_for_user[direction_for_user.replace(" ", "")][progression_for_user][interactiv_direction_for_user][0]) == 1: 
                await bot.send_message(message.chat.id, city_for_user[direction_for_user.replace(" ", "")][progression_for_user][0], reply_markup=markup)
            else:
                await bot.send_message(message.chat.id, city_for_user[direction_for_user.replace(" ", "")][progression_for_user][interactiv_direction_for_user], reply_markup=markup)
           
   
            if len(city_for_user[direction_for_user.replace(" ", "")][progression_for_user][interactiv_direction_for_user][0]) == 1:
                await bot.send_photo(message.chat.id, open(city_for_user[direction_for_user.replace(" ", "")][progression_for_user][1], 'rb'), reply_markup=markup)
            else:
                await bot.send_photo(message.chat.id, open(city_for_user[direction_for_user.replace(" ", "")][progression_for_user][interactiv_direction_for_user][0], 'rb'), reply_markup=markup)
        else:
            await bot.send_message(message.chat.id, "Пожалуйста пользуйтесь встроенными командами\n\nИли\n\nСкорее всего вы еще не оплатили экскурсию,\nсамое время это сделать")
            

    except FileNotFoundError:
        pass
    
    except IndexError:
        await bot.send_message(message.chat.id, "Экскурсия закончилась, ждем вас еще")
        db.MINUS(message.from_user.id, '-', 1)
        db.change_direction(message.from_user.id, '')
        await start_func(message)
        
        
    except KeyError:
        print(message.chat.id, "неправильно ввел", message.text)
        await bot.send_message(message.chat.id, "Пожалуйста, пользуйтесь командами")

if __name__ == '__main__':
    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)

