from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.types import ChatMemberAdministrator, ChatMemberOwner
from bot.utils.admin_check import can_restrict_check
from bot.utils.parse_time import parse_time

router = Router()

@router.message(Command("ban"))
@can_restrict_check
async def handle_ban(message: Message, command: CommandObject, *args, **kwargs):
    if not message.reply_to_message:
        return await message.answer("Неверный формат ввода команды! Пример: /ban <1m/1h/1d> где 1 - число единиц времени, m/h/d - единицы времени (минуты, часы, дни соответственно)")
    if message.reply_to_message.from_user.is_bot:
        return await message.answer("Данная команда применима только к пользователям.")
    
    member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
    if isinstance(member, ChatMemberAdministrator) or isinstance(member, ChatMemberOwner):
        return await message.answer("Данная команда применима только к пользователям без админских прав.")
    until_date = parse_time(command.args) if command.args else None
    if command.args and not until_date:
        return await message.answer("Неверный формат ввода времени! Пример: /ban <1m/1h/1d> где 1 - число единиц времени, m/h/d - единицы времени (минуты, часы, дни соответственно)")

    await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, until_date=until_date)
    await message.answer(f"Пользователь {message.reply_to_message.from_user.first_name} был успешно забанен админом {message.from_user.first_name}!")