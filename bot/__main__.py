import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from bot.handlers import start, mute, unmute, ban


load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
BOT_TOKEN = os.getenv("BOT_TOKEN")
async def main() -> None:
    if not BOT_TOKEN:
        raise ValueError("no bot token detected in .env file")
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_routers(start.router, mute.router, unmute.router, ban.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())