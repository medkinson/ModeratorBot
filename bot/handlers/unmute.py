from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions, ChatMemberOwner, ChatMemberAdministrator
from bot.utils.admin_check import can_restrict_check

router=Router()

UNMUTE_PERMS = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_other_messages=True,
    can_send_polls=True,
    can_add_web_page_previews=True,
    can_invite_users=True,
    can_change_info=True,
    can_pin_messages=True,
)

@router.message(Command("unmute"))
@can_restrict_check
async def handle_unmute(message: Message, *args, **kwargs) -> None:
    if not message.reply_to_message:
        return await message.answer("Данная команда применима только к ответу на сообщение.")
    if message.reply_to_message and message.reply_to_message.from_user.is_bot:
        return await message.answer("Данная команда применима только к пользователям.")
    
    member = await message.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)

    if (isinstance(member, ChatMemberAdministrator)) or (isinstance(member, ChatMemberOwner)):
        return await message.answer("Размьючивать можно только пользователей без админских прав.")
    
    await message.bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, permissions=UNMUTE_PERMS)
    await message.answer(f"{message.reply_to_message.from_user.first_name} был успешно размьючен админом {message.from_user.first_name}!")