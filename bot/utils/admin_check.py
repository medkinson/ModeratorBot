from aiogram.types import Message, ChatMemberAdministrator, ChatMemberOwner
from aiogram.filters import CommandObject

def can_restrict_check(func):
    async def wrapper(message: Message, command: CommandObject):
        bot = message.bot

        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if (isinstance(member, ChatMemberAdministrator) and member.can_restrict_members) or (isinstance(member, ChatMemberOwner)):
            return await func(message, command)
        else:
            await message.reply("govno, get admin perms first")
    return wrapper