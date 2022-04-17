import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from {{ cookiecutter.project_slug }}.models import User
from {{ cookiecutter.project_slug }}.telegram import bot


logger = logging.getLogger(__name__)


class LoggerMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        logger.info(f"{message.from_user.full_name} {message.text}", extra=data)
