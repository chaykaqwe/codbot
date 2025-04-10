from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.reqiest import get_random_ad, get_sponsor


async def ads_invite_kb():
    invite = await get_random_ad()
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=invite.invite_link_name, url=invite.invite_link)
    return keyboard.as_markup()


async def sponsor_invite_kb():
    invite = await get_sponsor()
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='подписаться', url=invite.name)
    return keyboard.as_markup()