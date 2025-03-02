import asyncio
import logging
from aiogram import Bot
from config import TK
from router import create_dispatcher


async def main():
    dp = create_dispatcher()
    bot = Bot(token=TK)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
