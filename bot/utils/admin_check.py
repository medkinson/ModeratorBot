from aiogram.types import Message, ChatMemberAdministrator, ChatMemberOwner

def can_restrict_check(func):
    async def wrapper(message: Message,*args, **kwargs):
        bot = message.bot

        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if (isinstance(member, ChatMemberAdministrator) and member.can_restrict_members) or (isinstance(member, ChatMemberOwner)):
            return await func(message,*args, **kwargs)
        else:
            return await message.reply("Вам требуются администраторские привилегии с возможностью ограничения прав пользователей.")
    return wrapper

def can_delete_messages_check(func):
    async def wrapper(message: Message, *args, **kwargs):
        bot = message.bot
        member = await bot.get_chat_member(chat_id=message.chat.id,user_id=message.from_user.id)

        if(isinstance(member, ChatMemberAdministrator) and member.can_delete_messages) or (isinstance(member, ChatMemberOwner)):
            return await func(message,*args, **kwargs)
        else:
            return await message.reply("Вам требуются администраторские привилегии с возможностью удаления сообщений.")
    return wrapper