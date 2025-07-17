from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, ChatPermissions
from bot.utils.admin_check import can_restrict_check
from bot.utils.parse_time import parse_time

router = Router()

@router.message(Command("mute"))
@can_restrict_check
async def handle_mute(message: Message, command: CommandObject) -> None:
    if not message.reply_to_message:
        return await message.answer("Неверный формат ввода команды! Пример: /mute <1m/1h/1d> - в ответ на сообщение, где 1 - число единиц времени, m/h/d - единицы времени (минуты, часы, дни соответственно)")
    if message.reply_to_message and message.reply_to_message.from_user.is_bot:
        return await message.answer("Данная команда применима только к пользователям.")
    
    until_date = parse_time(command.args) if command.args else None
    if command.args and not until_date:
        return await message.answer("Неверный формат ввода времени! Пример: /mute <1m/1h/1d> где 1 - число единиц времени, m/h/d - единицы времени (минуты, часы, дни соответственно)")

    await message.bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, permissions=ChatPermissions(can_send_messages=False), until_date=until_date)
    await message.answer(f"{message.reply_to_message.from_user.first_name} был успешно заткнут админом {message.from_user.first_name}!")