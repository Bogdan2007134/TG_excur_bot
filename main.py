import telebot
from telebot import types
from random import randint

from volgograd.data_text import *
bot = telebot.TeleBot("6259772380:AAHJIg_qvgJD-0ndlEJihRrTP8trb1JWgRY")

word_good = ["Интересно", "Прикольно", "Удивительно"]


class Progress(object):
    def __init__(self, direction="") -> None:
        self.progress = 0
        self.direction = direction
        self.condition = False

    def upgrade(self):
        self.progress += 1

    def progress_reset(self):
        self.progress = 0

    def reassignment(self, x):
        self.direction = x

    def buy(self, message):
        self.condition = True
        bot.send_message(message.chat.id, "Оплата успешно прошла")

    def end_buy(self):
        self.condition = False


user_progress = Progress()


@bot.message_handler(commands=['Купить_экскурсию'])  # Блок комманд
def buy_func(message):
    bot.send_message(
        message.chat.id, "В будущем тут будет система оплаты но будем\nсчитать что вы уже все оплатили")
    user_progress.buy(message)
    
@bot.message_handler(commands=['help'])  # Блок комманд
def help_func(message):
    # bot.send_message(message.chat.id, "")
    bot.send_photo(message.chat.id, open(volgograd[user_progress.direction.replace(" ", "")][user_progress.progress][2], 'rb'))
    


@bot.message_handler(commands=['start'])  # Блок комманд
def start_func(message):
    message_first = 'Приветствую в нашем боте, где вы находитесь?'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    volgograd = types.InlineKeyboardButton('/Волгоград')
    markup.add(volgograd)

    bot.send_message(message.chat.id, message_first, reply_markup=markup)


@bot.message_handler(commands=['Волгоград'])  # Блок комманд
def volgograd_func(message):
    message_first = 'Какой сценарий вы хотите выбрать?'
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=len(volgograd_list))
    buy_button = types.InlineKeyboardButton('/Купить_экскурсию')
    markup.add(buy_button)
    for i in volgograd_list:
        markup.add(i)

    bot.send_message(message.chat.id, message_first, reply_markup=markup)


@bot.message_handler(content_types=['text'])  # Блок комманд
def vol_Scen(message):
    try:
        if user_progress.condition == True and (message.text == "Военный сюжет" or message.text == "Романтический сюжет"):
            user_progress.progress_reset()
            user_progress.reassignment(message.text)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            next = types.InlineKeyboardButton(word_good[randint(0, len(word_good)-1)])
            markup.add(next)
            bot.send_message(
                message.chat.id, "Начнем нашу экскурсию", reply_markup=markup)

        elif message.text != "" and message.text != "Военный сюжет" and message.text != "Романтический сюжет":
            user_progress.upgrade()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            next = types.InlineKeyboardButton(word_good[randint(0, len(word_good)-1)])
            helping = types.InlineKeyboardButton("/help")
            markup.add(next, helping)
            
            bot.send_message(message.chat.id, volgograd[user_progress.direction.replace(" ", "")][user_progress.progress][0], reply_markup=markup)
            bot.send_photo(message.chat.id, open(volgograd[user_progress.direction.replace(" ", "")][user_progress.progress][1], 'rb'))
        else:
            bot.send_message(
                message.chat.id, "Скорее всего вы еще не оплатили экскурсию,\nсамое время это сделать")
    except FileNotFoundError:
        pass
    except IndexError:
        bot.send_message(
            message.chat.id, "Экскурсия закончилась, ждем вас еще")
        user_progress.end_buy()
        start_func(message)
    except KeyError:
        print(message.chat.id, "неправильно ввел", message.text)
        bot.send_message(message.chat.id, "Пожалуйста, пользуйтесь командами")
        start_func(message)


bot.polling(none_stop=True)
