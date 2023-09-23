from config import bot, db, ADMINS, NAME_BOT
from aiogram import types, Dispatcher
from txt_read.read_txt import read_txt_file
from KeyboardMarkup.KeyboardMarkup import mainMenu, navigation_menu, clear_reset_kb, clear_reset_promo_kb
from .excur import excur_Off_decorator
from KeyboardMarkup.KeyboardMarkup import admin_panel
from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from states.states import FeedbackState, PromocodeUser
import os
import asyncio

"""Обработчик команды /start"""
async def start_handler(msg: types.Message) -> None:
    if msg.chat.type == 'private':
        contents = await read_txt_file(['maintxt\\hello.txt'])
        if (not db.user_exists(msg.from_user.id)):
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            start_command = msg.text
            ref_id = str(start_command[7:])
            
            if str(ref_id) != '':
                if str(ref_id) != str(msg.from_user.id): 
                    db.add_user(msg.from_user.id, date, ref_id)
                    try:
                        count_ref = db.count_referrals(msg.from_user.id)
                        await bot.send_message(ref_id, f'''
🔥 Новый пользователь зарегистрировался по вашей ссылке!
👥 У вас уже рефералов: {count_ref} !
💰 При каждой их покупке экскурсии вам будет предоставлен промокод со случайной скидкой от 5% до 30%.
                                               ''') 
                    except:
                        pass
                else:
                    db.add_user(msg.from_user.id, date)
                    return await bot.send_message(msg.from_user.id, 'Нельзя регистрироваться по своей же ссылке!')  
            else:
                db.add_user(msg.from_user.id, date)
            
            await bot.send_message(msg.from_user.id, f"Приветствую вас, уважаемый путешественник {msg.from_user.first_name}🕵️‍♀️\n\n{contents[0]}", reply_markup=mainMenu())
            
            if msg.from_user.id in ADMINS:
                await bot.send_message(msg.from_user.id, '☑️Вы администратор!☑️', reply_markup=admin_panel())
                              
        elif (db.user_exists(msg.from_user.id)):
            await bot.send_message(msg.from_user.id, f"Приветствую вас снова, уважаемый путешественник {msg.from_user.first_name}🕵️‍♀️\n\n{contents[0]}", reply_markup=mainMenu())
            if msg.from_user.id in ADMINS:
                await bot.send_message(msg.from_user.id, '☑️Вы администратор!☑️', reply_markup=admin_panel())
            
"""Обработчики menu"""
async def navigation_menu_handler(msg: types.Message) -> None:
    await msg.delete()
    await msg.answer("Меню:", reply_markup=navigation_menu())

async def navigation_menu_callhandler(call: types.CallbackQuery) -> None:
    await call.message.answer("Меню:", reply_markup=navigation_menu())
    
async def send_feedback(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("""
✉️ Отправьте текст боту!
📝 Ваше сообщение будет передано администратору! 💌
💼 Не стесняйтесь поделиться своими впечатлениями, идеями или жалобой. 💭
                              """, reply_markup=clear_reset_kb())
    await FeedbackState.waiting_for_feedback.set()
    

async def handle_feedback_message(msg: types.Message, state: FSMContext):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton("Ответить", callback_data=f'support_' + str(msg.from_user.id) + '%' + str(msg.from_user.first_name)),
    )
    if  types.ContentType.TEXT == msg.content_type: 
        for admin in ADMINS:
            await bot.send_message(chat_id=admin, text=f"""
🔔 Новое обращение получено 🔔

📅 Дата: {date}
👤 Имя: {msg.from_user.first_name}
🆔 ID: {msg.from_user.id}
💬 Сообщение: {msg.text}

🚀 Пожалуйста, обратите внимание на это обращение и предоставьте ответ в самое ближайшее время.

Спасибо! 🙏
        """, reply_markup=keyboard)        
        
    elif types.ContentType.PHOTO == msg.content_type:
        text = f"""
🔔 Новое обращение получено 🔔

📅 Дата: {date}
👤 Имя: {msg.from_user.first_name}
🆔 ID: {msg.from_user.id}
💬 Сообщение: {msg.html_text if msg.caption else ' '}

🚀 Пожалуйста, обратите внимание на это обращение и предоставьте ответ в самое ближайшее время.

Спасибо! 🙏
        """
        for admin in ADMINS:
            await bot.send_photo(
                chat_id=admin,
                photo=msg.photo[-1].file_id,
                caption=text
            )
    elif types.ContentType.VIDEO == msg.content_type:
        text = f"""
🔔 Новое обращение получено 🔔

📅 Дата: {date}
👤 Имя: {msg.from_user.first_name}
🆔 ID: {msg.from_user.id}
💬 Сообщение: {msg.html_text if msg.caption else ' '}

🚀 Пожалуйста, обратите внимание на это обращение и предоставьте ответ в самое ближайшее время.

Спасибо! 🙏
        """
        for admin in ADMINS:
            await bot.send_video(
                chat_id=admin,
                video=msg.video.file_id,
                caption=text
            )
    elif types.ContentType.STICKER == msg.content_type: 
        for admin in ADMINS:
            await bot.send_sticker(
                chat_id=admin,
                sticker=msg.sticker.file_id
            )
    else:
        await msg.answer(
            '<b>Формат сообщения не поддерживается!</b>'
        )
        
     
    await msg.answer(f"""
📅 {date} 📅

_______________________________

💌 Сообщение отправлено модераторам бота 💌 

Ваше сообщение успешно доставлено модераторам бота. Мы постараемся ответить вам в ближайшее время.

Спасибо за обращение!
                        """)
    await state.finish() 
@excur_Off_decorator
async def set_PromoUser(call: types.CallbackQuery):
    await PromocodeUser.promocode.set()
    await call.message.answer('Введите промокод или номер купона на скидку:', reply_markup=clear_reset_kb())    
    
    
async def set_PromoUser_desc(msg: types.Message, state: FSMContext):  
    promocode = msg.text 
    promo = db.get_promo_discount_dict()
    msgs =  await msg.answer('<b>Поиск...</b>')
    if promocode in promo:
        if not promocode in db.get_promocode_user(msg.from_user.id):
            if db.get_usage_by_promo(promocode) != 101:
                promo_discount = promo[f'{promocode}']
                await msgs.delete()
                if db.get_usage_by_promo(promocode) == 1:
                    db.add_to_promocode(msg.from_user.id, promocode)
                    db.add_current_promo(msg.from_user.id, promocode)
                    db.update_usage_by_promo(promocode, 101)
                    await msg.answer(f'🎉 Поздравляем! \nВы успешно ввели личный промокод "{promocode}" и получили скидку в размере {promo_discount}%! 🎁', reply_markup=mainMenu())   
                    await asyncio.sleep(0.15)
                else:
                    db.add_to_promocode(msg.from_user.id, promocode)
                    db.add_current_promo(msg.from_user.id, promocode)
                    await msg.answer(f'🎉 Поздравляем! \nВы успешно ввели промокод "{promocode}" и получили скидку в размере {promo_discount}%! 🎁', reply_markup=mainMenu()) 
                await state.finish()
            else:
                await msgs.delete()
                await msg.answer(f'''
Промокод "{promocode}" недействительный! 😔
Попробуйте ввести другой промокод или обратитесь в поддержку. 💬
                                ''', reply_markup=clear_reset_promo_kb()) 
        else:
            await msgs.delete()
            await msg.answer(f'''
Вы уже использовали промокод "{promocode}"!
Введите другой промокод или обратитесь в поддержку!
                            ''', reply_markup=clear_reset_promo_kb()) 
    else:
        await msgs.delete()
        await msg.answer(f'''
Промокод "{promocode}" не найден!😔
Попробуйте еще раз 🔁 или обратитесь в поддержку. 
                         ''', reply_markup=clear_reset_promo_kb()) 
    
 
async def give_promocode_refer_handler(call: types.CallbackQuery,):
    await call.message.answer(f'''
🌟 Реферальная ссылка: https://t.me/{NAME_BOT}?start={call.from_user.id} 🌟

👥 Количество рефералов: {db.count_referrals(call.from_user.id)}

🎁 Приглашайте пользователей по вашей реферальной ссылке и получайте бесплатные промокоды! После каждой их покупки экскурсии вы будите получать уведомления с уникальными промокодами, предоставляющими случайные скидки от 5% до 30%.

✨ Не упускайте возможность порадовать себя и ваших друзей удивительными скидками на захватывающие путешествия! ✨                  
                         ''') 
   
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands='start')
    dp.register_message_handler(navigation_menu_handler, commands='menu')
    dp.register_callback_query_handler(navigation_menu_callhandler, text='backformenu')
    
    dp.register_callback_query_handler(send_feedback, text='send_feedback')
    dp.register_message_handler(handle_feedback_message, state=FeedbackState.waiting_for_feedback, content_types=types.ContentType.ANY)
    
    dp.register_callback_query_handler(set_PromoUser, text='promocode')
    dp.register_message_handler(set_PromoUser_desc, state=PromocodeUser.promocode)
    
    dp.register_callback_query_handler(give_promocode_refer_handler, text='givepromocode')
    
    