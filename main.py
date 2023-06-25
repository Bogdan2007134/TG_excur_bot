import telebot
from telebot import types
from random import randint

from volgograd.data_text import *
bot = telebot.TeleBot("6259772380:AAHJIg_qvgJD-0ndlEJihRrTP8trb1JWgRY")

word_good = ["Интересно", "Прикольно", "Удивительно"]

all_users = {}

@bot.message_handler(commands=['start'])  # Блок комманд
def start_func(message):

    try:
        all_users[message.chat.id]['progress']
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        volgograd = types.InlineKeyboardButton('/Волгоград')
        markup.add(volgograd)
        
        bot.send_message(message.chat.id, f'Приветствую тебя повторно {message.chat.first_name} в нашем боте', reply_markup=markup)
        
    except KeyError:
        all_users[message.chat.id] = {'progress': 0,
                                    'direction': "",
                                    'condition' : False,
                                    'interactiv_direction' : 0,
                                    }
    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        volgograd = types.InlineKeyboardButton('/Волгоград')
        markup.add(volgograd)
        
        bot.send_message(message.chat.id, f'Приветствую тебя {message.chat.first_name} в нашем боте', reply_markup=markup)

@bot.message_handler(commands=['Волгоград'])  # Блок комманд
def volgograd_func(message):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=len(volgograd_list))
    if all_users[message.chat.id]["direction"] == "":
        buy_button = types.InlineKeyboardButton('/Купить_экскурсию')
        
        markup.add(buy_button)
        for i in volgograd_list:
            markup.add(i)
            
        bot.send_message(message.chat.id, 'Какой сценарий вы хотите выбрать?', reply_markup=markup)
    else:
        markup.add(all_users[message.chat.id]["direction"])
        bot.send_message(message.chat.id, "Какой именно вы сценарий хотите допройти?", reply_markup=markup)

@bot.message_handler(commands=['Купить_экскурсию'])  # Блок комманд
def buy_func(message):
    try:
        bot.send_message(message.chat.id, "В будущем тут будет система оплаты но будем\nсчитать что вы уже все оплатили")
        all_users[message.chat.id]['condition'] = True
        bot.send_message(message.chat.id, "Оплата успешно прошла")
    except KeyError as key:
        bot.send_message(message.chat.id, "Извините за неудобства, но начните сначала")
        print(f"[ERROR] error in buy_func {key}")
        start_func(message)
    




@bot.message_handler(content_types=['text'])  # Блок комманд
def vol_Scen(message):
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
            bot.send_message(
                message.chat.id, "Начнем нашу экскурсию", reply_markup=markup)
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
                bot.send_message(message.chat.id, volgograd[all_users[message.chat.id]['direction'].replace(" ", "")][all_users[message.chat.id]['progress']][0], reply_markup=markup)
            else:
                bot.send_message(message.chat.id, volgograd[all_users[message.chat.id]['direction'].replace(" ", "")][all_users[message.chat.id]['progress']][all_users[message.chat.id]['interactiv_direction']], reply_markup=markup)
           
   
            if len(volgograd[all_users[message.chat.id]['direction'].replace(" ", "")][all_users[message.chat.id]['progress']][all_users[message.chat.id]['interactiv_direction']][1]) == 1:
                bot.send_photo(message.chat.id, open(volgograd[all_users[message.chat.id]['direction'].replace(" ", "")][all_users[message.chat.id]['progress']][1], 'rb'), reply_markup=markup)
            else:
                bot.send_photo(message.chat.id, open(volgograd[all_users[message.chat.id]['direction'].replace(" ", "")][all_users[message.chat.id]['progress']][all_users[message.chat.id]['interactiv_direction']][1], 'rb'), reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Пожалуйста пользуйтесь встроенными командами\n\nИли\n\nСкорее всего вы еще не оплатили экскурсию,\nсамое время это сделать")
            

    except FileNotFoundError:
        pass
    
    except IndexError:
        bot.send_message(message.chat.id, "Экскурсия закончилась, ждем вас еще")
        all_users[message.chat.id]['condition'] = False
        all_users[message.chat.id]['direction'] = ""
        start_func(message)
        
    except KeyError:
        print(message.chat.id, "неправильно ввел", message.text)
        bot.send_message(message.chat.id, "Пожалуйста, пользуйтесь командами")


bot.polling(none_stop=True)
