from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message
from aiogram.filters import CommandObject
from bot.database.models import ModeratorStats

# Луиджи Чесноков был здесь

def users_in_db_required(func):
    """
    Decorator that ensures both the executing user and the replied-to user have ModeratorStats entries in the database for the current chat before calling the decorated async handler.
    
    If either user does not exist in the ModeratorStats table, a new entry with zero warns is created and committed.
    """
    async def wrapper(message: Message, command: CommandObject, session: AsyncSession, *args, **kwargs):
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
        