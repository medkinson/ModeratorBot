from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions
from bot.utils.user_checks import reply_required, replied_user_is_not_bot_required, replied_user_is_not_admin_required
from bot.utils.perm_checks import restrict_perm_required

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
@reply_required
@replied_user_is_not_bot_required
@replied_user_is_not_admin_required
@restrict_perm_required
async def handle_unmute(message: Message, *args, **kwargs) -> None:
    await message.bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, permissions=UNMUTE_PERMS)
    await message.answer(f"{message.reply_to_message.from_user.first_name} был успешно размьючен админом {message.from_user.first_name}!")