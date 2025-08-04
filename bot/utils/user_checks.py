from aiogram import Bot
from aiogram.types import Message, ChatMemberAdministrator, ChatMemberOwner

def reply_required(func):
    async def wrapper(message: Message, *args, **kwargs):
        if message.reply_to_message:
            return await func(message, *args, **kwargs)
        else:
            await message.answer("Данная команда применима только в ответ на сообщение.")
    return wrapper

def replied_user_is_not_admin_required(func):
    async def wrapper(message: Message, *args, **kwargs):
        member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
        if isinstance(member, ChatMemberAdministrator) or isinstance(member, ChatMemberOwner):
            return await message.answer("Данная команда применима только к пользователям без админских прав.")
        else:
            await func(message, *args, **kwargs)
    return wrapper

def replied_user_is_not_bot_required(func):
    async def wrapper(message: Message, *args, **kwargs):
        if message.reply_to_message.from_user.is_bot:
            return await message.answer("Данная команда применима только к пользователям.")
        else:
            await func(message, *args, **kwargs)
    return wrapper
