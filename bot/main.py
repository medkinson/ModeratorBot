import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers import start
#from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
#from middlewares.db import DbSessionMiddleware
#from database.models import CrowbarStats, Base

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

async def main() -> None:

    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    dp.include_routers(start.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())