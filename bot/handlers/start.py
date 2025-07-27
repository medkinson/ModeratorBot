import random
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer("✅ ОНЛАЙН")