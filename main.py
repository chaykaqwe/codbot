import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.hundlers import router
from app.database.models import async_main


async def main():
    load_dotenv()
    await async_main()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
