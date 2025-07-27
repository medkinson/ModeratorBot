from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message
from aiogram.filters import CommandObject
from bot.database.models import ModeratorStats

def are_users_in_db(func):
    async def wrapper(message: Message, session: AsyncSession, command: CommandObject, *args, **kwargs):
        chat_id = message.chat.id
        user_id = message.from_user.id

        executing_user = await session.get(ModeratorStats, {"chat_id": chat_id, "telegram_id": user_id})
        if not executing_user:
            executing_user = ModeratorStats(
                chat_id=chat_id,
                telegram_id=user_id,
                warns=0
            )
            session.add(executing_user)
            await session.commit()
        
        if not message.reply_to_message:
            return await message.answer("Данная команда применима только в ответ на сообщение.")
        
        replied_user_id = message.reply_to_message.from_user.id

        replied_user = await session.get(ModeratorStats, {"chat_id": chat_id, "telegram_id": replied_user_id})
        if not replied_user:
            replied_user = ModeratorStats(
                chat_id=chat_id,
                telegram_id=replied_user_id,
                warns=0
            )
            session.add(replied_user)
            await session.commit()
        return await func(message, command, session, *args, **kwargs)
    return wrapper
        