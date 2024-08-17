from sqlalchemy import select, update
from db.models import Users, Progress_users, Promocodes, Excursions
from print_colorama import error, info
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import FSInputFile


async def get_direction(session: AsyncSession, user_id):

    try:
        result = await session.execute(
            select(Progress_users.direction).where(
                Progress_users.user_id == user_id)
        )

        progress = result.scalars().first()
        return progress
    except SQLAlchemyError as e:
        error(f"Юзер не найден! Ошибка: {e}")


async def get_progress(session: AsyncSession, user_id):

    try:
        result = await session.execute(
            select(Progress_users.progress).where(
                Progress_users.user_id == user_id)
        )

        progress = result.scalars().first()
        return progress
    except SQLAlchemyError as e:
        error(f"Юзер не найден! Ошибка: {e}")


async def update_progression(session: AsyncSession, user_id):

    progress = await get_progress(session, user_id)

    try:
        query = (
            update(Progress_users).
            where(Progress_users.user_id == user_id).
            values(progress=progress+1)
        )
        await session.execute(query)
        await session.commit()
        info(f"Новый пользователь перешел дальше id:{user_id}")
    except SQLAlchemyError as e:
        error(f"Юзер не найден! Ошибка: {e}")


async def reset_progression(session: AsyncSession, user_id):
    try:
        query = (
            update(Progress_users).
            where(Progress_users.user_id == user_id).
            values(progress=0)
        )
        await session.execute(query)
        await session.commit()
        info(f"Новый пользователь закончил экскурсию id:{user_id}")
    except SQLAlchemyError as e:
        error(f"Юзер не найден! Ошибка: {e}")


async def reset_direction(session: AsyncSession, user_id):
    try:
        query = (
            update(Progress_users).
            where(Progress_users.user_id == user_id).
            values(direction="")
        )
        await session.execute(query)
        await session.commit()
    except SQLAlchemyError as e:
        error(f"Юзер не найден! Ошибка: {e}")


async def get_media(media):
    return FSInputFile(
        "src/bot/client/resources/" + media)

async def delete_promo(session: AsyncSession, promocode: str):
    try:
        query = (
            update(Promocodes).
            where(Promocodes.promocode == promocode).
            values(is_active=False)
        )
        await session.execute(query)
        await session.commit()
    except SQLAlchemyError as e:
        error(f"Error: {e}")


async def check_promo(session: AsyncSession, promocode: str) -> bool:
    try:
        result = await session.execute(
            select(Promocodes).where(Promocodes.promocode == promocode)
        )
        promo = result.scalars().first()
        return bool(promo)
    except SQLAlchemyError as e:
        error(f"Error: {e}")
        return False

async def get_excur_name(session: AsyncSession, excur_id: int):
    try:
        result = await session.execute(
            select(Excursions.name).where(Excursions.excur_id == excur_id)
        )
        name = result.scalars().first()
        return name
    except SQLAlchemyError as e:
        error(f"Error: {e}")
