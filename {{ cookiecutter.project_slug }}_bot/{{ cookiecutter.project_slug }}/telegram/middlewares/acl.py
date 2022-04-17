import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from {{ cookiecutter.project_slug }}.models import User
from {{ cookiecutter.project_slug }}.telegram import bot

logger = logging.getLogger(__name__)


class ACLMiddleware(BaseMiddleware):
    async def setup_chat(self, data: dict, user: types.User, message: types.Message):
        user_id = user.id

        member = await bot.get_chat_member(message.chat.id, message.from_user.id)

        user = (
            await User.get_or_create(
                id=user_id,
                defaults={
                    "username": user.username,
                    "full_name": user.full_name,
                    "language": user.language_code,
                    "is_active": True,
                    "role": "admin" if member.is_chat_admin() else "user",
                }
            )
        )[0]

        data["user"] = user

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(data, message.from_user, message)
