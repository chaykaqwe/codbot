from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.reqiest import get_random_ad


async def invite_kb():
    invite = await get_random_ad()
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=invite.invite_link_name, url=invite.invite_link)
    return keyboard.as_markup()
