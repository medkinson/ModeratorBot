from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from sqlalchemy.ext.asyncio import AsyncSession
from bot.utils.admin_check import can_delete_messages_check
from bot.utils.db import are_users_in_db
from bot.database.models import ModeratorStats

router = Router()
WARN_LIMIT = 3


@router.message(Command("warn"))
@are_users_in_db
@can_delete_messages_check
async def handle_warn(message: Message, command: CommandObject, session: AsyncSession, *args, **kwargs):
    if message.reply_to_message.from_user.is_bot:
        return await message.answer("Данная команда применима только к пользователям.")
    
    replied_user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    replied_user = await session.get(ModeratorStats, {"chat_id": chat_id, "telegram_id": replied_user_id})
    if replied_user.warns < WARN_LIMIT:
        replied_user.warns += 1
        await session.commit()
        await message.answer(f"{message.reply_to_message.from_user.first_name} был предупрежден администратором {message.from_user.first_name}! Теперь у {message.reply_to_message.from_user.first_name} {replied_user.warns}/{WARN_LIMIT} предупреждений!")
    elif replied_user.warns >= WARN_LIMIT:
        await message.answer("У данного пользователя уже максимум предупреждений! Примите необходимые действия.")