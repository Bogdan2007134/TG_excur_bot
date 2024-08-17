import re
import datetime
import random

from print_colorama import error, info

from aiogram import Router, Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.types import (
    Message,
    CallbackQuery,
    Update,
    LabeledPrice,
    PreCheckoutQuery,
    ShippingOption,
    ShippingQuery,
    InputMediaPhoto,
)

from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.exceptions import TelegramBadRequest
from fastapi import Depends

from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils.chat_type import ChatTypeFilter
from utils.read_txt import read_txt_file

from config.config import settings

from .keyboards import main_kb, start_excur_kb, next_slide_kb, interactive_slide_kb

from db.models import Users, Progress_users, Promocodes

from .tools import get_direction, reset_direction, get_progress, update_progression, reset_progression, get_media

from .resources.excur.excur import excur


router = Router()
router.message.filter(ChatTypeFilter(["private"]))

PATH = "src/bot/client/resources/"

"""Главное меню"""
@router.message(CommandStart())
async def start_command(
    message: Message, bot: Bot, session: AsyncSession, command: CommandObject, state: FSMContext
):
    args = command.args
    user_id = message.from_user.id
    if user_id:
        try:
            result = await session.execute(
                select(Users).where(Users.user_id == user_id)
            )
            result = result.scalars().first()
        except SQLAlchemyError as e:
            error(f"Юзер не найден! Ошибка: {e}")

        if (not result):
            try:
                query = insert(Users).values(
                    user_id=message.from_user.id,   
                    username=message.from_user.username,
                                   
                )
                await session.execute(query)
                await session.commit()
                info(f"Новый пользователь добавлен в таблицу 'users' id:{user_id}")
            except SQLAlchemyError as e:
                error(e)
                error("Ошибка при внесении данных в базу данных!")

        if not args:
            if not user_id in settings.ADMIN_ID:
                text_user = await read_txt_file(settings.HELLO_PATH)
                photo = FSInputFile(settings.MAIN_PHOTOS)
                return await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo,
                    caption=text_user,
                    reply_markup=main_kb(),
                )

            if user_id in settings.ADMIN_ID:
                text_admin = await read_txt_file(settings.ADMIN_HELLO_PATH)
                return await message.answer(text_admin, reply_markup=None)

        if args:
            # начало экскурсии
            print(args)
            # сохраняем в состояния наш код
            # args = promocode1_username1
            username_args, promo_code = args.split("_")
            username = message.from_user.username

            # [(1, "BNTVDD133BLMMQOKIPWY", "pythontelegramm", 76353)]
            try:
                promo_list = select(Promocodes.id,
                                    Promocodes.promocode,
                                    Promocodes.username,
                                    Promocodes.excur_id
                                    )
                result = await session.execute(promo_list)
                promo_list = result.all()
            except SQLAlchemyError as e:
                error(e)
                error("Ошибка при внесении данных в базу данных!")
            print(promo_list)

            print(promo_code, username, username_args)

            for promo_id, promo_code_db, username_db, excur_id in promo_list:
                print(promo_code_db, username_db)
                print(promo_code, username)
                if promo_code == promo_code_db and username == username_db:

                    await state.update_data(promo_code=promo_code)
                    await state.update_data(username_args=username_args)
                    await state.update_data(excur_id=excur_id)

                    try:
                        query = insert(Progress_users).values(
                            user_id=message.from_user.id,
                            ref_id="",
                            direction="Набережная Ялты, еë секреты и тайны Крым",
                            progress=0,
                            active=1,
                            condition=1,
                            payment_status=1,
                            page=2,
                            current_promo=0,
                            promocode="",
                            date="2023-09-23 23:16:50"
                        )
                        await session.execute(query)
                        await session.commit()
                    except SQLAlchemyError as e:
                        error(e)
                        error("Ошибка при внесении данных в базу данных!")

                    info(f"Новый пользователь начал экскурсию id:{user_id}")

                    return await bot.send_message(
                        message.from_user.id,
                        "Начать экскурсию?",
                        reply_markup=next_slide_kb(text="Начать!"),
                    )
                    # НАДО БУДЕТ СПРЯТАТЬ КНОПКУ НАЧАТЬ ПОСЛЕ НАЧАЛА ЭКСКУРСИИ
                    
            return await message.answer("Неверный промокод или он не ваш!")


def shuffle_lists(list1, list2):
    combined = list(zip(list1, list2))
    random.shuffle(combined)
    shuffled_list1, shuffled_list2 = zip(*combined)
    return list(shuffled_list1), list(shuffled_list2)


interactiv_list = ["interactiv_1", "interactiv_2", "interactiv_3"]


@router.callback_query(F.data == "next_slide")
@router.callback_query(F.data == "interactiv_1")
@router.callback_query(F.data == "interactiv_2")
@router.callback_query(F.data == "interactiv_3")
async def start_excur(callback: CallbackQuery, bot: Bot, session: AsyncSession):
    user_id = callback.from_user.id

    def check_condition():
        return callback.data == "interactiv_1" or callback.data == "next_slide"

    progress = await get_progress(session, user_id)
    direction = await get_direction(session, user_id)
    chat_id = callback.message.chat.id
    slide_now = ''
    moved = 0
    if check_condition():
        moved = 0
    else:
        moved = -1
    try:
        slide_now = excur[direction][progress + moved]
    except IndexError:
        await reset_progression(session, user_id)
        await reset_direction(session, user_id)
    text_slide = await read_txt_file(PATH + str(slide_now[0]))

    info(
        f"Пользователь {user_id} по имени {callback.from_user.first_name}\nпутешествует по {direction}\nи находится на стадии {progress}, нажав команду {callback.data}"
    )
    info("\n\n\n")

    keyboard = ""

    try:

        if isinstance(slide_now[-1], list):
            inter = slide_now[-1]
            shuffled_list1, shuffled_list2 = shuffle_lists(
                inter, interactiv_list)
            keyboard = interactive_slide_kb(shuffled_list1, shuffled_list2)

        else:
            keyboard = next_slide_kb(slide_now[-1])

    except IndexError:
        pass
    try:

        if isinstance(slide_now[1], list) and len(slide_now[1]) > 1:

            if str(slide_now[1][0][-4:]) == '.png':

                video = await get_media(slide_now[1][1])
                image = await get_media(slide_now[1][0])

                await bot.send_photo(user_id, photo=image)
                await bot.send_video(user_id, video=video, caption=text_slide, reply_markup=keyboard)
                await bot.edit_message_reply_markup(chat_id=chat_id, message_id=str(callback.message.message_id), reply_markup=None)
                await update_progression(session, user_id) if check_condition() else 0

            elif str(slide_now[1][0][-4:]) == '.mp4':

                video = await get_media(slide_now[1][0])
                image = await get_media(slide_now[1][1])

                await bot.send_video(chat_id=user_id, video=video)
                await bot.send_photo(chat_id=user_id, photo=image, caption=text_slide, reply_markup=keyboard)
                await bot.edit_message_reply_markup(chat_id=chat_id, message_id=str(callback.message.message_id), reply_markup=None)
                await update_progression(session, user_id) if check_condition() else 0

        else:

            if str(slide_now[1][0])[-4:] == ".png":

                image = await get_media(slide_now[1][0])

                await bot.send_photo(user_id, photo=image, caption=text_slide, reply_markup=keyboard)
                await bot.edit_message_reply_markup(chat_id=chat_id, message_id=str(callback.message.message_id), reply_markup=None)
                await update_progression(session, user_id) if check_condition() else 0

            elif str(slide_now[1][0])[-4:] == ".mp4":

                video = await get_media(slide_now[1][0])

                await bot.send_video(user_id, video=video, caption=text_slide, reply_markup=keyboard)
                await bot.edit_message_reply_markup(chat_id=chat_id, message_id=str(callback.message.message_id), reply_markup=None)
                await update_progression(session, user_id) if check_condition() else 0

            else:

                audio = await get_media(slide_now[1][0])

                await bot.send_audio(user_id, audio=audio, caption=text_slide, reply_markup=keyboard)
                await bot.edit_message_reply_markup(chat_id=chat_id, message_id=str(callback.message.message_id), reply_markup=None)
                await update_progression(session, user_id) if check_condition() else 0

    except:
        await bot.send_message(chat_id=user_id, text=text_slide, reply_markup=keyboard)
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=str(callback.message.message_id), reply_markup=None)
        await update_progression(session, user_id) if check_condition() else 0


# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# @router.message(Command("media"))
# async def media_test_func(
# message: Message,
# bot: Bot,
# session: AsyncSession,
# command: CommandObject,
# state: FSMContext,
# ):
# media_group = MediaGroupBuilder(caption="Фото и видео")
# media_group.add(type="video", media=FSInputFile("video_1.mp4"))
# media_group.add(type="photo", media=FSInputFile("photo_0.png"))
#
# await bot.send_media_group(
# chat_id=message.chat.id,
# media=media_group.build(),
# )
#
#
#
#
