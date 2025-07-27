import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from bot.handlers import start, mute, unmute, ban, warn
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from bot.middlewares.db import DbSessionMiddleware
from bot.database.models import Base

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

DB_URL = os.getenv("DB_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")

engine = create_async_engine(DB_URL, echo=True)
sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

async def main() -> None:
    if not DB_URL:
        raise ValueError("no db url detected in .env file")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    if not BOT_TOKEN:
        raise ValueError("no bot token detected in .env file")
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.update.middleware(DbSessionMiddleware(sessionmaker))
    dp.include_routers(start.router, mute.router, unmute.router, ban.router, warn.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())