from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions
from aiogram.methods import restrict_chat_member
from bot.utils.admin_check import can_restrict_check

router = Router()

@router.message(Command("mute"))
@can_restrict_check
async def handle_mute(message: Message) -> None:
    await message.bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, permissions=ChatPermissions(can_send_messages=False))
    await message.answer(f"Successfully muted {message.reply_to_message.from_user.first_name} by admin {message.from_user.first_name}!")