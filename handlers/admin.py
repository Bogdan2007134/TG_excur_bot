from config import bot, db, ADMINS
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from txt_read.read_txt import read_txt_file
from KeyboardMarkup.KeyboardMarkup import admin_panel, clear_reset_kb, promocode_admin
from states.states import (
    Mail,
    UpdateExcur,
    UsersSupport,
    PromocodeAdmin,
    DELETEPromocodeAdmin,
)
import asyncio
import re
from datetime import datetime

"""Блоки комманд Админа"""


async def admin_panel_handler(msg: types.Message):
    if msg.from_user.id in ADMINS:
        Admin_help = await read_txt_file(["maintxt\\admin_help.txt"])

        await bot.send_message(
            msg.from_user.id, f"{Admin_help[0]}", reply_markup=admin_panel()
        )
        await msg.delete()
    else:
        await msg.reply(
            f"<b>Я не понимаю вас❗️</b>\n <b>❗️Возможно вы тот самый {msg.from_user.first_name}</b>"
        )


async def add_price(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id in ADMINS:
        await UpdateExcur.price.set()
        await call.message.answer(
            "Напишите цену всех экскурсий в рублях:", reply_markup=clear_reset_kb()
        )
    else:
        await call.message.reply(
            f"<b>Я не понимаю вас❗️</b>\n <b>❗️Возможно вы тот самый {call.from_user.first_name}</b>"
        )


async def add_price_desc(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["price"] = int(msg.text) * 100
    await msg.answer("Изменения вступили в силу!")

    data = await state.get_data()
    prices = int(data.get("price"))

    db.add_price(1, +prices)

    await state.finish()


"""Рассылка"""


async def mail_handler(call: types.CallbackQuery):
    await bot.send_message(
        call.from_user.id,
        "<b>❗️Отправьте сообщение для рассылки❗️</b>",
        reply_markup=clear_reset_kb(),
    )
    await Mail.mail.set()


async def mail_on(message: types.Message, state: FSMContext):
    if types.ContentType.TEXT == message.content_type:  # Если админ отправил текст
        for user in db.get_users():
            try:
                await bot.send_message(chat_id=user[0], text=message.html_text)
                if int(user[0] != 1):
                    db.set_active(user[0], 1)
                await asyncio.sleep(0.33)
            except:
                db.set_active(user[0], 0)
        else:
            await message.answer("<b>✅ Рассылка завершена!</b>")
            await state.finish()
    elif types.ContentType.PHOTO == message.content_type:  # Если админ отправил фото
        print(1)
        for user in db.get_users():
            try:
                await bot.send_photo(
                    chat_id=user[0],
                    photo=message.photo[-1].file_id,
                    caption=message.html_text if message.caption else None,
                )
                if int(user[0] != 1):
                    db.set_active(user[0], 1)
                await asyncio.sleep(0.33)
            except:
                db.set_active(user[0], 0)
        else:
            await message.answer("<b>✅ Рассылка завершена!</b>")
            await state.finish()

    elif types.ContentType.VIDEO == message.content_type:  # Если админ отправил видео
        for user in db.get_users():
            try:
                await bot.send_video(
                    chat_id=user[0],
                    video=message.video.file_id,
                    caption=message.html_text if message.caption else None,
                )
                if int(user[0] != 1):
                    db.set_active(user[0], 1)
                await asyncio.sleep(0.33)
            except:
                db.set_active(user[0], 0)
        else:
            await message.answer("<b>✅ Рассылка завершена!</b>")
            await state.finish()

    elif types.ContentType.ANIMATION == message.content_type:  # Если админ отправил gif
        for user in db.get_users():
            try:
                await bot.send_animation(
                    chat_id=user[0],
                    animation=message.animation.file_id,
                    caption=message.html_text if message.caption else None,
                )
                if int(user[0] != 1):
                    db.set_active(user[0], 1)
                await asyncio.sleep(0.33)
            except:
                db.set_active(user[0], 0)
        else:
            await message.answer("<b>✅ Рассылка завершена!</b>")
            await state.finish()

    else:
        await message.answer(
            "<b>❗️Данный формат контента не поддерживается для рассылки</b>"
        )
        await state.finish()


async def send_statistics_users(call: types.CallbackQuery):
    users_count = db.get_user_count()
    users_last_day = db.get_users_last_day_count()
    users_last_week = db.get_users_last_week_count()
    users_last_month = db.get_users_last_month_count()
    users_last_year = db.get_users_last_year_count()

    await call.message.answer(
        f"""<b>
╔══════════════════════╗
║ Всего пользователей •{users_count}
╠══════════════════════╣
║ За последний день •{users_last_day}  
║ За последнюю неделю •{users_last_week}  
║ За последний месяц •{users_last_month} 
║ За последний год  •{users_last_year}  
╚══════════════════════╝
</b>"""
    )


async def send_statistics_excursion(call: types.CallbackQuery):
    excur_statistic_count = db.get_excur_statistic_count()
    excur_statisticlast_day = db.get_excur_statistic_last_day()
    excur_statisticlast_week = db.get_excur_statistic_last_week()
    excur_statistic_last_month = db.get_excur_statistic_last_month()
    excur_statistic_last_year = db.get_excur_statistic_last_year()

    income_from_excursions = db.get_total_excur_price()

    await call.message.answer(
        f"""<b>
╔══════════════════════╗
║ Всего купленно •{excur_statistic_count}
╠══════════════════════╣
║ За последний день •{excur_statisticlast_day}   
║ За последнюю неделю •{excur_statisticlast_week}  
║ За последний месяц •{excur_statistic_last_month}
║ За последний год  •{excur_statistic_last_year}   
╠══════════════════════╣
║Итог: {income_from_excursions}₽
╚══════════════════════╝
</b>"""
    )


async def support_handler(call: types.CallbackQuery, state: FSMContext):
    callback_data = call.data.strip()
    match = re.match(r"^support_(.*)$", callback_data)
    match_list = match.group(1).split("%")
    print(match_list)
    await UsersSupport.id_support.set()
    async with state.proxy() as data:
        data["id_support"] = int(match_list[0])
    print(match_list[0])
    print(match_list[1])
    await UsersSupport.usesname.set()
    async with state.proxy() as data:
        data["usesname"] = str(match_list[1])

    await call.message.answer("Введите текст ответа:", reply_markup=clear_reset_kb())
    await UsersSupport.response_text.set()


async def support_message_handler(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    id_support = data.get("id_support")
    first_name = data.get("usesname")
    print(id_support)
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if types.ContentType.TEXT == msg.content_type:
        text = f"""
Уведомление для пользователя:

📅 Дата: {date}

👤 Уважаемый(ая) {first_name},

Мы рады сообщить вам, что ваше сообщение получило ответ от администратора. 

💬 Текст ответа: {msg.html_text}

Если у вас возникнут дополнительные вопросы, пожалуйста, не стесняйтесь обращаться к нам. Мы всегда готовы помочь.

С уважением,
Команда поддержки бота       
        """
        try:
            await bot.send_message(chat_id=id_support, text=text)
            await asyncio.sleep(0.33)
        except:
            await msg.answer("<b>Ошибка: возможно пользователя больше нет в боте!</b>")
            await state.finish()

        await msg.answer("<b>✅ Ответ отправлен!</b>")
        await state.finish()
    elif types.ContentType.PHOTO == msg.content_type:  # Если админ отправил фото
        text = f"""
Уведомление для пользователя:

📅 Дата: {date}

👤 Уважаемый(ая) {first_name},

Мы рады сообщить вам, что ваше сообщение получило ответ от администратора. 

💬 Текст ответа: {msg.html_text if msg.caption else ' '}

Если у вас возникнут дополнительные вопросы, пожалуйста, не стесняйтесь обращаться к нам. Мы всегда готовы помочь.

С уважением,
Команда поддержки бота       
        """
        try:
            await bot.send_photo(
                chat_id=id_support, photo=msg.photo[-1].file_id, caption=text
            )
            await asyncio.sleep(0.33)
        except:
            await msg.answer("<b>Ошибка: возможно пользователя больше нет в боте!</b>")
            await state.finish()

        await msg.answer("<b>✅ Ответ отправлен!</b>")
        await state.finish()

    elif types.ContentType.VIDEO == msg.content_type:  # Если админ отправил видео
        text = f"""
Уведомление для пользователя:

📅 Дата: {date}

👤 Уважаемый(ая) {first_name},

Мы рады сообщить вам, что ваше сообщение получило ответ от администратора. 

💬 Текст ответа: {msg.html_text if msg.caption else 'Текст отсутвует'}

Если у вас возникнут дополнительные вопросы, пожалуйста, не стесняйтесь обращаться к нам. Мы всегда готовы помочь.

С уважением,
Команда поддержки бота       
        """
        try:
            await bot.send_video(
                chat_id=id_support, video=msg.video.file_id, caption=text
            )
            await asyncio.sleep(0.33)
        except:
            await msg.answer("<b>Ошибка: возможно пользователя больше нет в боте!</b>")
            await state.finish()

        await msg.answer("<b>✅ Ответ отправлен!</b>")
        await state.finish()

    elif types.ContentType.STICKER == msg.content_type:  # Если админ отправил стикер
        try:
            await bot.send_sticker(chat_id=id_support, sticker=msg.sticker.file_id)
            await asyncio.sleep(0.33)
        except:
            await msg.answer("<b>Ошибка: возможно пользователя больше нет в боте!</b>")
            await state.finish()

        await msg.answer("<b>✅ Ответ отправлен!</b>")
        await state.finish()
    else:
        await msg.answer("<b>Формат сообщения не поддерживается!</b>")


async def panel_promocode(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id in ADMINS:
        promo = db.get_promo_discount_dict()
        output = ""
        for key, value in promo.items():
            output += f"•{key}: {value}%\n"
        await call.message.answer(
            f"<b>Текущие промокоды\n─────────────\n{output}</b>",
            reply_markup=promocode_admin(),
        )


async def add_promocode(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id in ADMINS:
        await PromocodeAdmin.promo.set()
        await call.message.answer(
            "<b>Напишите название для нового промокода:</b>",
            reply_markup=clear_reset_kb(),
        )


async def add_promocode_desc_promo(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["promo"] = msg.text
    await PromocodeAdmin.discount.set()
    await msg.answer(
        "<b>Введите скидку для промокода от 0 до 100 (без %):</b>",
        reply_markup=clear_reset_kb(),
    )


async def add_promocode_desc_discount(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if int(msg.text) >= 0 and int(msg.text) <= 100:
            data["discount"] = int(msg.text)
            await PromocodeAdmin.usage.set()
            await msg.answer(
                "<b>Введите будет ли промокод удаляться после 1 использования(да или нет)</b>",
                reply_markup=clear_reset_kb(),
            )
        else:
            await msg.answer(
                "<b>Некорректное значение для скидки. Введите число от 0 до 100.</b>"
            )


async def add_promocode_desc_usage(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if str(msg.text) == "да" or "нет" or "Да" or "Нет":
            data["usage"] = str(msg.text)
            try:
                data = await state.get_data()
                promo = str(data.get("promo"))
                discount = int(data.get("discount"))
                usage = str(data.get("usage"))
                if usage == "да" or "Да":
                    usage = 1
                else:
                    usage = 0

                db.add_promocode(promo, discount, usage)
                await msg.answer("<b>✅ Промокод успешно создан!</b>")
                await state.finish()

            except ValueError:
                await msg.answer(
                    "<b>Какая-то ошибка: попробуйте снова или лезте в код!</b>"
                )

        else:
            await msg.answer("<b>Можно отвечать только да или нет!</b>")


async def delete_promocode(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id in ADMINS:
        await DELETEPromocodeAdmin.promo_delete.set()
        await call.message.answer(
            "<b>Напишите название промокода который хотите удалить:</b>",
            reply_markup=clear_reset_kb(),
        )


async def delete_promocode_desc(msg: types.Message, state: FSMContext):
    try:
        promo_msg_delete = msg.text
        promo = db.get_promo_discount_dict()
        if promo_msg_delete in promo:
            db.delete_promocode(promo_msg_delete)
            await msg.answer("<b>🗑 Промокод успешно удален!</b>")
            await state.finish()
        else:
            await msg.answer("<b>Вы ввели несуществующий промокод!</b>")
    except:
        await msg.answer(
            "<b>Возможно промокод несуществует или возникла другая ошибка!</b>"
        )


def register_handlers_admins(dp: Dispatcher):
    dp.register_message_handler(admin_panel_handler, text=["admin", "/admin"])

    dp.register_callback_query_handler(add_price, text="select_price")
    dp.register_message_handler(add_price_desc, state=UpdateExcur.price)

    dp.register_callback_query_handler(mail_handler, text="rassilka")
    dp.register_message_handler(
        mail_on, state=Mail.mail, content_types=types.ContentType.ANY
    )

    dp.register_callback_query_handler(
        send_statistics_users, text="send_statistics_users"
    )
    dp.register_callback_query_handler(
        send_statistics_excursion, text="send_statistics_excursion"
    )

    dp.register_callback_query_handler(
        support_handler, lambda c: c.data.startswith("support_")
    )
    dp.register_message_handler(
        support_message_handler,
        state=UsersSupport.response_text,
        content_types=types.ContentType.ANY,
    )

    dp.register_callback_query_handler(panel_promocode, text="admin_promocode")

    dp.register_callback_query_handler(add_promocode, text="insert_promocode")
    dp.register_message_handler(add_promocode_desc_promo, state=PromocodeAdmin.promo)
    dp.register_message_handler(
        add_promocode_desc_discount, state=PromocodeAdmin.discount
    )
    dp.register_message_handler(add_promocode_desc_usage, state=PromocodeAdmin.usage)

    dp.register_callback_query_handler(delete_promocode, text="delete_promocode")
    dp.register_message_handler(
        delete_promocode_desc, state=DELETEPromocodeAdmin.promo_delete
    )
