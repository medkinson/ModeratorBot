from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from sqlalchemy.ext.asyncio import AsyncSession
from bot.utils.perm_checks import delete_perm_required
from bot.utils.user_checks import reply_required, replied_user_is_not_admin_required, replied_user_is_not_bot_required
from bot.utils.db import users_in_db_required
from bot.database.models import ModeratorStats

router = Router()
WARN_LIMIT = 3


@router.message(Command("warn"))
@reply_required
@replied_user_is_not_bot_required
@replied_user_is_not_admin_required
@users_in_db_required
@delete_perm_required
async def handle_warn(message: Message, command: CommandObject, session: AsyncSession, *args, **kwargs):
    replied_user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    replied_user = await session.get(ModeratorStats, {"chat_id": chat_id, "telegram_id": replied_user_id})

    reason = command.args

    if replied_user.warns == WARN_LIMIT-1:
        replied_user.warns += 1
        await session.commit()
        return await message.answer(
        f"{message.reply_to_message.from_user.first_name} был успешно предупрежден админом {message.from_user.first_name} "+
        (f"по причине: {reason}! Достигнут максимум предупреждений - примите действия!" if reason else "без указания причины! Достигнут максимум предупреждений - примите действия!")           
        )

    elif replied_user.warns < WARN_LIMIT:
        replied_user.warns += 1
        await session.commit()
        return await message.answer(
        f"{message.reply_to_message.from_user.first_name} был успешно предупрежден админом {message.from_user.first_name} "+
        (f"по причине: {reason}! Теперь у него {replied_user.warns}/{WARN_LIMIT} предупреждений!" if reason else f"без указания причины! Теперь у него {replied_user.warns}/{WARN_LIMIT} предупреждений!")           
        )

    else:
        await message.answer(f"У {message.reply_to_message.from_user.first_name} и так максимум предупреждений! Примите меры!")