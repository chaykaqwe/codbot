from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
import asyncio
import os
from dotenv import load_dotenv
from aiogram.exceptions import TelegramBadRequest
from app.bot import bot

from app.database.reqiest import get_cods, get_random_ad, get_sponsor, set_user
import app.keybord as kb

router = Router(name=__name__)
load_dotenv()
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME')


@router.message(CommandStart())
async def cmd(mes: Message):
    await set_user(mes.from_user.id)
    await mes.answer('Добро пожаловать! Введите код ')
    asyncio.create_task(send_advertisement(mes))


@router.message(F.text)
async def giv_cod(message: Message):
    sponsor_access = await check_subscription(message.from_user.id)
    if sponsor_access:
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
    else:
        sponsor = await get_sponsor()
        await message.answer(f'подпишитесь на спосноров {sponsor.name}')


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


async def check_subscription(user_id: int):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        else:
            return False
    except TelegramBadRequest:  # Если чат не найден или есть ошибка
        return False
