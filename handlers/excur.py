import os
import random
from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import bot, db
from excur.data_text import excur
from states.states import ReviewForExcursions
from KeyboardMarkup.KeyboardMarkup import back_for_menu
from txt_read.read_txt import read_txt_file


def shuffle_lists(list1, list2):
    combined = list(zip(list1, list2))
    random.shuffle(combined)
    shuffled_list1, shuffled_list2 = zip(*combined)
    return list(shuffled_list1), list(shuffled_list2)


interactiv_list = ["interactiv_1", "interactiv_2", "interactiv_3"]


def excur_Off_decorator(function):
    async def wrapper(msg: types.Message):
        await function(msg) if db.select_condition(msg.from_user.id)[0][0] == False else await bot.send_message(msg.from_user.id, "Пожалуйста закончи экскурсию")
    return wrapper


def excur_ON_decorator(function):
    async def wrapper(message: types.Message):
        await function(message) if db.select_payment_status(message.from_user.id)[0][0] == True else await bot.send_message(message.from_user.id, "Возможно ты не оплатил экскурсию или она уже началась!")
    return wrapper


@excur_ON_decorator
async def help_excur(call: types.CallbackQuery):
    user_id = call.from_user.id
    progress = db.select_progress(user_id)
    direction = db.select_direction(user_id)
    text = await read_txt_file([str(excur[direction][progress[0][0]][3])])
    text = text[0]
    map_image = open(str(excur[direction][progress[0][0]][2]), 'rb')
    keyboard_excur = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Вернуться к экскурсии", callback_data="excur_back")
            ],
            [
                InlineKeyboardButton(
                    text='Обратиться в поддержку', callback_data='send_feedback')
            ],
        ],
        resize_keyboard=True
    )
    if not os.path.exists(str(excur[direction][progress[0][0]][1])):
        print("Файл не найден:", video)
        await bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)
        await bot.send_photo(chat_id=user_id, photo=map_image, caption=text, reply_markup=keyboard_excur)
    else:
        video = open(str(excur[direction][progress[0][0]][4]), 'rb')
        await bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)
        await bot.send_video(chat_id=user_id, video=video)
        await bot.send_photo(chat_id=user_id, photo=map_image, caption=text, reply_markup=keyboard_excur)


@excur_ON_decorator
async def excur_algorithm(call: types.CallbackQuery):
    user_id = call.from_user.id
    db.add_condition(user_id, True)
    progress = db.select_progress(user_id)
    direction = db.select_direction(user_id)
    print(
f'\nПользователь {user_id} по имени {call.from_user.first_name}\nпутешествует по {direction}\nи находится на стадии {progress[0][0]}, нажав команду {call.data}\n')

    def reset_progression(): return db.reset_progress(user_id)
    def update_progression(): return db.update_progress(user_id)

    try:
        text = await read_txt_file([str(excur[direction][progress[0][0]][0])])
        text = text[0]

        keyboard_excur = None
        if isinstance(excur[direction][progress[0][0]][-1], list):
            inter = excur[direction][progress[0][0]][-1]
            shuffled_list1, shuffled_list2 = shuffle_lists(
                inter, interactiv_list)

            keyboard_excur = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=shuffled_list1[0], callback_data=shuffled_list2[0])
                    ],
                    [
                        InlineKeyboardButton(
                            text=shuffled_list1[1], callback_data=shuffled_list2[1])
                    ],
                    [
                        InlineKeyboardButton(
                            text=shuffled_list1[2], callback_data=shuffled_list2[2])
                    ],
                ],
                resize_keyboard=False
            )
        else:
            keyboard_excur = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=excur[direction][progress[0][0]][-1], callback_data="excur_start")
                    ],
                    [
                        InlineKeyboardButton(
                            text='Я потерялся', callback_data='help_excur')
                    ],
                ],
                resize_keyboard=True
            )

        if call.data == "excur_start" or call.data == "excur_back":
            if excur[direction][progress[0][0]][1]:
                for element in excur[direction][progress[0][0]][1]:
                    if element == excur[direction][progress[0][0]][1][-1]:
                        caption = text
                        reply = keyboard_excur
                    else:
                        caption = None
                        reply = None
                    if str(element[-4:]) == '.png':
                        image = open(str(element), 'rb')
                        await bot.send_photo(chat_id=user_id, photo=image, caption=caption, reply_markup=reply)

                    if str(element[-4:]) == '.mp4':
                        video = open(str(element), 'rb')
                        await bot.send_video(chat_id=user_id, video=video, caption=caption, reply_markup=reply)
                        
                    if str(element[-4:]) == '.mp3':
                        audio = open(str(element), 'rb')
                        await bot.send_audio(chat_id=user_id, audio=audio, caption=caption, reply_markup=reply)
            else:
                await bot.send_message(user_id, text=text, reply_markup=keyboard_excur)
            await bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)
            update_progression()

        elif call.data in ["interactiv_1", "interactiv_2", "interactiv_3"]:
            if call.data == "interactiv_1":
                if excur[direction][progress[0][0]][1]:
                    for element in excur[direction][progress[0][0]][1]:
                        if element == excur[direction][progress[0][0]][1][-1]:
                            caption = text
                            reply = keyboard_excur
                        else:
                            caption = None
                            reply = None
                        if str(element[-4:]) == '.png':
                            image = open(str(element), 'rb')
                            await bot.send_photo(chat_id=user_id, photo=image, caption=caption, reply_markup=reply)

                        if str(element[-4:]) == '.mp4':
                            video = open(str(element), 'rb')
                            await bot.send_video(chat_id=user_id, video=video, caption=caption, reply_markup=reply)
                            
                        if str(element[-4:]) == '.mp3':
                            audio = open(str(element), 'rb')
                            await bot.send_audio(chat_id=user_id, audio=audio, caption=caption, reply_markup=reply)

                else:
                    await bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard_excur)
                await bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)
                update_progression()

            else:
                try:
                    inter = excur[direction][progress[0][0] - 1][-1]
                    shuffled_list1, shuffled_list2 = shuffle_lists(
                        inter, interactiv_list)
                    keyboard_excur = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text=shuffled_list1[0], callback_data=shuffled_list2[0])
                            ],
                            [
                                InlineKeyboardButton(
                                    text=shuffled_list1[1], callback_data=shuffled_list2[1])
                            ],
                            [
                                InlineKeyboardButton(
                                    text=shuffled_list1[2], callback_data=shuffled_list2[2])
                            ],
                        ],
                        resize_keyboard=False
                    )
                    image = open(
                        str(excur[direction][progress[0][0] - 1][1]), 'rb')
                    await bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)
                    await bot.send_photo(chat_id=user_id, photo=image, caption="Это неверный вариант ответа, будьте внимательны, попробуйте еще раз.", reply_markup=keyboard_excur)
                except:
                    await bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)
                    await bot.send_message(chat_id=user_id, text="Это неверный вариант ответа, будьте внимательны, попробуйте еще раз.", reply_markup=keyboard_excur)

    except IndexError or UnboundLocalError:
        reset_progression()
        await bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)
        keyboard_score = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='⭐️☆☆☆☆', callback_data='score_1')
                ],
                [
                    InlineKeyboardButton(
                        text='⭐️⭐️☆☆☆', callback_data='score_2')
                ],
                [
                    InlineKeyboardButton(
                        text='⭐️⭐️⭐️☆☆', callback_data='score_3')
                ],
                [
                    InlineKeyboardButton(
                        text='⭐️⭐️⭐️⭐️☆', callback_data='score_4')
                ],
                [
                    InlineKeyboardButton(
                        text='⭐️⭐️⭐️⭐️⭐️', callback_data='score_5')
                ],
            ],
            resize_keyboard=False,
            row_width=1
        )
        await bot.send_message(user_id, """
🙏 Пожалуйста, оцените нашу экскурсию! 

⭐️ Ваш отзыв очень важен для нас, чтобы сделать наши экскурсии еще лучше! 

🙌 Благодарим вас заранее!
                               """, reply_markup=keyboard_score)


async def feedback_excur_handler(call: types.CallbackQuery, state: FSMContext):
    await ReviewForExcursions.name.set()
    async with state.proxy() as data:
        data['name'] = call.from_user.first_name

    await ReviewForExcursions.login.set()
    async with state.proxy() as data:
        data['login'] = f'@{call.from_user.username}'

    scores_dict = {
        "score_1": "⭐️☆☆☆☆",
        "score_2": "⭐️⭐️☆☆☆",
        "score_3": "⭐️⭐️⭐️☆☆",
        "score_4": "⭐️⭐️⭐️⭐️☆",
        "score_5": "⭐️⭐️⭐️⭐️⭐️",
    }

    if call.data in scores_dict:
        await ReviewForExcursions.scores.set()
        async with state.proxy() as data:
            data['scores'] = scores_dict[call.data]

    await ReviewForExcursions.excursus.set()
    async with state.proxy() as data:
        data['excursus'] = db.select_direction(call.from_user.id)

    await call.message.answer('Введите текст для отзыва:')
    await ReviewForExcursions.feedback_text.set()


async def feedback_excur_send_handler(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    data = await state.get_data()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    name = data.get('name')
    login = data.get('login')
    scores = data.get('scores')
    excursus = data.get('excursus')

    await bot.send_message(chat_id='-1001908997143', text=f"""
🌟🌟🌟 НОВЫЙ ОТЗЫВ 🌟🌟🌟

 📅 Дата: {date}

🔖 Имя: {name}

👤 Юзернейм: {login}

⭐️ Оценка: {scores}

 🌍 Экскурсия: {excursus}

💬 Отзыв: {msg.text}

------------------------
✨ Благодарим за отзыв! ✨

RSS
    """)

    db.add_condition(user_id, False)
    db.add_payment_status(user_id, False)
    db.add_direction(user_id, '')
    await bot.send_message(user_id, """
🔚 К сожалению экскурсия подошла к концу. Надеемся, что она вам понравилась! 

🙌 Ждем вас снова, чтобы рассказать еще больше интересных историй! Если у вас есть вопросы или пожелания, обращайтесь к нашей команде. 

👍 Ваши отзывы очень важны для нас, помогите нам стать лучше! Спасибо, что выбрали нас!

------------------------
🌟 Благодарим вас за оценку экскурсии! 🌟

RSS
    """, reply_markup=back_for_menu())
    await state.finish()


def register_handlers_excur(dp: Dispatcher):
    dp.register_callback_query_handler(
        excur_algorithm, lambda c: c.data.startswith('excur_start') or c.data.startswith(
            'excur_back') or c.data.startswith('interactiv_1') or c.data.startswith('interactiv_2')
        or c.data.startswith('interactiv_3'))
    dp.register_callback_query_handler(
        help_excur, lambda c: c.data.startswith("help_excur"))
    dp.register_callback_query_handler(
        feedback_excur_handler, lambda c: c.data.startswith("score_"))
    dp.register_message_handler(
        feedback_excur_send_handler, state=ReviewForExcursions.feedback_text)
