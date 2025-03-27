from app.database.models import async_session
from app.database.models import Cod, Advertising
from sqlalchemy import select, func
import random


async def get_cods(code_id):
    async with async_session() as session:
        return await session.scalar(select(Cod).where(Cod.id == code_id))


async def get_random_ad():
    """Выбирает случайную рекламу из базы данных"""
    async with async_session() as session:
        count = await session.scalar(select(func.count()).select_from(Advertising))
        if count == 0:
            return None  # Если нет объявлений, возвращаем None

        random_index = random.randint(0, count - 1)
        ad = await session.scalar(select(Advertising).offset(random_index).limit(1))
        return ad