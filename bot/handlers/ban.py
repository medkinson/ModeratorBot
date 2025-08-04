from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from bot.utils.perm_checks import restrict_perm_required
from bot.utils.user_checks import reply_required, replied_user_is_not_bot_required, replied_user_is_not_admin_required
from bot.utils.parse_time import parse_time

router = Router()

@router.message(Command("ban"))
@reply_required
@replied_user_is_not_bot_required
@replied_user_is_not_admin_required
@restrict_perm_required
async def handle_ban(message: Message, command: CommandObject, *args, **kwargs):
    if command.args:
        arguments = command.args.split(maxsplit=2)
        time = arguments[0]
        reason = arguments[1] if len(arguments) > 1 else None
    else:
        return await message.answer("Неверный формат ввода команды! Пример: /ban <1m/1h/1d> <причина>, где 1 - число единиц времени, m/h/d - единицы времени (минуты, часы, дни соответственно)")
    until_date = parse_time(time)
    if not until_date:
        return await message.answer("Неверный формат ввода времени! Пример: /ban <1m/1h/1d> <причина>, где 1 - число единиц времени, m/h/d - единицы времени (минуты, часы, дни соответственно)")

    await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, until_date=until_date)
    await message.answer(
        f"Пользователь {message.reply_to_message.from_user.first_name} был успешно забанен админом {message.from_user.first_name} "+
        (f"по причине: {reason}!" if reason else "без указания причины!")
        )