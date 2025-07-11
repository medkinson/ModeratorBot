import random
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def handle_start(message: Message) -> None:
    await message.answer("tor")