from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
import asyncio


from app.database.reqiest import get_cods, get_random_ad
import app.keybord as kb

router = Router(name=__name__)


@router.message(CommandStart())
async def cmd(mes: Message):
    await mes.answer('Добро пожаловать! Введите код ')
    asyncio.create_task(send_advertisement(mes))


@router.message(F.text)
async def giv_cod(message: Message):
    code_id_str = message.text
    try:
        code_id = int(code_id_str)
    except ValueError:
        await message.answer("Пожалуйста, введите числовой id.")
        return

    cod = await get_cods(code_id)
    if cod:
        await message.answer(f"Название: {cod.name}")
    else:
        await message.answer("Код с таким id не найден.")


async def send_advertisement(message: Message):
    """Фоновая задача: отправляет рекламу через 60 секунд"""
    await asyncio.sleep(60)  # Ждём 60 секунд
    ad = await get_random_ad()
    if ad:
        text = f"{ad.name}"
        if ad.image_url and ad.invite_link:
            await message.answer_photo(photo=ad.image_url, caption=text, reply_markup=await kb.invite_kb())
            asyncio.create_task(send_advertisement(message))
        else:
            await message.answer(text)
            asyncio.create_task(send_advertisement(message))