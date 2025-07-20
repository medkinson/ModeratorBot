from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, ChatPermissions, ChatMemberAdministrator, ChatMemberOwner
from bot.utils.admin_check import can_restrict_check
from bot.utils.parse_time import parse_time

router = Router()

MUTE_PERMS = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_other_messages=False,
    can_send_polls=False,
)

@router.message(Command("mute"))
@can_restrict_check
async def handle_mute(message: Message, command: CommandObject, *args, **kwargs) -> None:
    if not message.reply_to_message:
        return await message.answer("Неверный формат ввода команды! Пример: /mute <1m/1h/1d> <причина>, - в ответ на сообщение, где 1 - число единиц времени, m/h/d - единицы времени (минуты, часы, дни соответственно)")
    if message.reply_to_message and message.reply_to_message.from_user.is_bot:
        return await message.answer("Данная команда применима только к пользователям.")
    
    member = await message.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)

    if (isinstance(member, ChatMemberAdministrator)) or (isinstance(member, ChatMemberOwner)):
        return await message.answer("Затыкать можно только пользователей без админских прав.")
    
    if command.args:
        arguments = command.args.split(maxsplit=2)
        time = arguments[0]
        reason = arguments[1] if len(arguments) > 1 else None
    else:
        return await message.answer("Неверный формат ввода команды! Пример: /mute <1m/1h/1d> <причина>, - в ответ на сообщение, где 1 - число единиц времени, m/h/d - единицы времени (минуты, часы, дни соответственно)")

    until_date = parse_time(time)
    if not until_date:
        return await message.answer("Неверный формат ввода времени! Пример: /mute <1m/1h/1d> <причина>, где 1 - число единиц времени, m/h/d - единицы времени (минуты, часы, дни соответственно)")

    await message.bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, permissions=MUTE_PERMS, until_date=until_date)
    await message.answer(
        f"{message.reply_to_message.from_user.first_name} был успешно заткнут админом {message.from_user.first_name} "+
        (f"по причине: {reason}!" if reason else "без указания причины!")           
        )