from aiogram import Bot
from aiogram.types import ChatMemberAdministrator, ChatMemberOwner
from functools import wraps
from aiogram.types import Message

def can_restrict_check():
    def decorator(func):
        @wraps(func)
        async def wrapper(message: Message):
            bot = message.bot

            member = await bot.get_chat_member(message.chat.id, message.from_user.id)
            if (isinstance(member, ChatMemberAdministrator) and member.can_restrict_members) or (isinstance(member, ChatMemberOwner)):
                return await func(message)
            else:
                await message.reply("govno, get admin perms first")
        return wrapper
    return decorator
