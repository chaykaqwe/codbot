import asyncio
from app.bot import bot, dp  # Импортируем бот и диспетчер
from app.hundlers import router
from app.database.models import async_main


async def main():
    await async_main()
    dp.include_router(router)
    await dp.start_polling(bot)  # Запускаем бота

if __name__ == "__main__":
    asyncio.run(main())
