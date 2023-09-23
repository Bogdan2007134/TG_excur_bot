from config import bot, YOOTOKEN, db
from aiogram import types, Dispatcher
from aiogram.types.message import ContentType
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
from .excur import excur_Off_decorator
from lists_dictionaries.check_excur_lists import excur_names_dict
import re
from random import randint, choice
import string

async def generate_promo_code():
    characters = string.ascii_letters + string.digits
    promo_code = ''.join(choice(characters) for _ in range(8))
    return promo_code

@excur_Off_decorator
async def pay_excur(call: types.CallbackQuery):
    callback_data = call.data.strip()
    match = re.match(r'^buy_(.*)$', callback_data)
    excur_name = match.group(1)
    title = f'Оплата экскурсии {excur_name}'
    price = db.get_price(1) 
    try:
        check_promo = db.get_current_promo_user(call.from_user.id)
        promo = db.get_promo_discount_dict()
        print(promo)
        print(check_promo)
        if check_promo in promo:
            promo_discount = promo[f'{check_promo}']
            price = int(price - (price * promo_discount / 100))
            title += f' (скидка по промокоду {promo_discount}%)'
            print(promo_discount)
    except IndexError:
        price = db.get_price(1) 
           
    if match:
        payload = 'pay_' + excur_name
        await bot.send_invoice(
            chat_id=call.from_user.id,
            title=title,
            description='После оплаты экскурсия начнётся когда вы будете готовы!',
            payload=payload,
            provider_token=YOOTOKEN,
            currency='RUB',
            start_parameter='Excur_bot',
            prices=[{"label": "Руб", "amount": price}]
        )

async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def process_pay(msg: types.Message):
    try:
        check_promo = db.get_current_promo_user(msg.from_user.id)
        promo = db.get_promo_discount_dict()
        price = db.get_price(1) / 100 
        if check_promo in promo:
            promo_discount = promo[f'{check_promo}']
            price = int((price - (price * promo_discount / 100)))
    except IndexError:
        price = price 
        
    db.delete_promocode(check_promo)    
    payload = msg.successful_payment.invoice_payload
    match = re.match(r'^pay_(.*)$', payload)
   
    excur_name = match.group(1)
    
    if excur_name in excur_names_dict:
        excur_names = excur_names_dict[excur_name]
    else:
        excur_names = ''
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Начать', callback_data='excur_start')
            ],
        ],
        resize_keyboard=True
    )
    try:     
        ref_id = db.get_ref_id_user(msg.from_user.id)
        print(ref_id)
        if str(ref_id) != '':
            promocode = await generate_promo_code()
            discount = randint(5, 30)
            db.add_promocode(promocode, discount, 1)
            await bot.send_message(int(ref_id), f'''
🌍 Поздравляю! Ваш реферал только что приобрел экскурсию! 🌍

Используйте промокод: ```{promocode}``` 🎁
Количество рефералов: {db.count_referrals(msg.from_user.id)} 👥

Продолжайте приглашать еще больше людей на наши увлекательные экскурсии! ✈️

                                                    ''', parse_mode=types.ParseMode.MARKDOWN)

    except:
        pass        
    
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.add_current_promo(msg.from_user.id, None)
    db.add_direction(msg.from_user.id, excur_names)
    db.add_payment_status(msg.from_user.id, True)
    db.add_condition(msg.from_user.id, True)
    db.add_excursion(date, price)
    
    print(db.get_direction(msg.from_user.id))
    await msg.answer(f'''
Вы оплатили экскурсию {excur_names} ✨

Спасибо за покупку!  🙏🏻

Когда будете готовы начать экскурсию, нажмите кнопку "Начать" ▶️
                     ''', reply_markup=keyboard)

def register_payment_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(pay_excur, lambda c: c.data.startswith('buy_'))
    dp.register_pre_checkout_query_handler(process_pre_checkout_query)
    dp.register_message_handler(process_pay, content_types=ContentType.SUCCESSFUL_PAYMENT)