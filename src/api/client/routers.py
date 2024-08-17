from print_colorama import error, info

from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy import select, insert, update, text, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_
from sqlalchemy import case
from sqlalchemy.sql.expression import null
from sqlalchemy.sql import bindparam
from sqlalchemy.exc import SQLAlchemyError

from db.models import Excursions as Excursions_models
from db.models import Promocodes as Promocodes_models

from db.database import get_async_session

from config.config import settings

from .schemas import Excursions, DeleteExcursion, EditExcursion, SuccessfulPayment
from .utils import save_img, get_promo_code 


router = APIRouter(prefix="/excursion", tags=["excursion"])


async def get_static_img_url(filename: str) -> str:
    return f"{settings.APP_URL}/{filename}"


@router.get(
    "/",
    summary="Получение всех экскурсий",
    description="",
    status_code=200,)
async def get_excursion(session: AsyncSession = Depends(get_async_session)):
    query = select(
        Excursions_models.id,
        Excursions_models.excur_id,
        Excursions_models.name,
        Excursions_models.description,
        Excursions_models.price,
        Excursions_models.photo,
    )
    result = await session.execute(query)
    rows = result.all()
    excursions = [
        {
            "id": row.id,
            "excur_id": row.excur_id,
            "name": row.name,
            "description": row.description,
            "price": row.price,
            "photo": await get_static_img_url(row.photo),
        }
        for row in rows
    ]
    return {"excursions": excursions}


@router.post(
    "/successful_payment",
    summary="Создание промокода для экскурсии после успешной оплаты и генерация ссылки",
    description="",
    status_code=201,)
async def successful_payment(
    data: SuccessfulPayment = Body(...), session: AsyncSession = Depends(get_async_session)
):
    promocode = get_promo_code(20)
    query = insert(Promocodes_models).values(
        promocode=promocode,
        username=data.username,
        excur_id=data.excur_id           
    )
    await session.execute(query)
    await session.commit()

    return {
        "url_bot": f"https://t.me/{settings.BOT_NAME}?start={data.username}_{promocode}"
    }


@router.post(
    "/add_excursions",
    summary="Добавление новых экскурсий",
    description="",
    status_code=201,
)
async def add_excursions(
    excursions: Excursions = Body(...),
    session: AsyncSession = Depends(get_async_session),
):
    for excursion in excursions.excursions:
        photo_path = rf"{settings.STATIC_FOLDER}/img/{excursion.excur_id}_photo.png"
        photo_path_url = rf"static/img/{excursion.excur_id}_photo.png"

        try:
            await save_img(excursion.photo, photo_path)
        except Exception as e:
            error(f"Error saving image: {e}")
            raise HTTPException(status_code=500, detail="Error saving image")

        try:
            query = insert(Excursions_models).values(
                excur_id=excursion.excur_id,
                name=excursion.name,
                description=excursion.description,
                price=excursion.price,
                photo=photo_path_url
            )
            await session.execute(query)
            await session.commit()
        except SQLAlchemyError as e:
            error(f"Error saving excursion: {e}")
            raise HTTPException(status_code=500, detail="Error saving excursion")

    return {"detail": "Successfully"}


@router.post(
    "/delete_excursions",
    summary="Удаление экскурсий",
    description="",
    status_code=200,
)
async def delete_excursions(excur_id: DeleteExcursion = Body(...), session: AsyncSession = Depends(get_async_session)):
    query = delete(Excursions_models).where(Excursions_models.excur_id == excur_id.excur_id)
    await session.execute(query)
    await session.commit()
    return {"detail": f"Tour with ID {excur_id} successfully deleted"}

@router.post(
    "/edit_excursions",
    summary="Редактирование экскурсий",
    description="",
    status_code=200,
)
async def edit_excursions(
    excur_data: EditExcursion, session: AsyncSession = Depends(get_async_session)):
    query = select(Excursions_models).where(Excursions_models.excur_id == excur_data.excur_id)
    result = (await session.execute(query)).all()

    if result:
        try:
            query = update(Excursions_models).where(Excursions_models.excur_id == excur_data.excur_id)
            if excur_data.name:
                query = query.values(name=excur_data.name)
            if excur_data.description:
                query = query.values(description=excur_data.description)
            if excur_data.price:
                query = query.values(price=excur_data.price)
            await session.execute(query)
            await session.commit()
        except SQLAlchemyError as e:
            error(f"Error editing excursion: {e}")
            raise HTTPException(status_code=500, detail="Error editing excursion")
    else:
        raise HTTPException(status_code=404, detail="Excursion not found")
    return {"detail": f"Tour with ID {excur_data.excur_id} successfully edited"}
