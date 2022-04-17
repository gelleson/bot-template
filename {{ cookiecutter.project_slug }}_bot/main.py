import logging

from tortoise import Tortoise
from aiogram.utils.executor import Executor
from aiogram import Dispatcher
from aiogram.dispatcher.webhook import get_new_configured_app, BOT_DISPATCHER_KEY
from aiohttp import web
from aiohttp.web_app import Application

from {{cookiecutter.project_slug}}.telegram.middlewares import ACLMiddleware, LoggerMiddleware
from {{cookiecutter.project_slug}}.telegram.app import bot
from {{cookiecutter.project_slug}}.telegram.filters import IsAdmin
from {{cookiecutter.project_slug}} import settings
from {{cookiecutter.project_slug}}.db.config import TORTOISE_ORM
from {{cookiecutter.project_slug}}.utils import logger as logger_config


logger_config.install()

logger = logging.getLogger(__name__)


async def init(dp: Dispatcher):
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        config=TORTOISE_ORM,
    )

    dp.middleware.setup(ACLMiddleware())
    dp.middleware.setup(LoggerMiddleware())
    dp.bind_filter(IsAdmin)


async def on_startup(application: Application):
    dp = application[BOT_DISPATCHER_KEY]
    await init(dp)

    webhook = await bot.get_webhook_info()
    if webhook.url != settings.TELEGRAM_WEBHOOK_URL:
        await bot.delete_webhook()
        await bot.set_webhook(url=settings.TELEGRAM_WEBHOOK_URL)
        logging.info("Webhook set")


if __name__ == '__main__':
    from {{cookiecutter.project_slug}}.telegram import dispatcher

    executor = Executor(dispatcher)

    executor.on_startup(init)

    if settings.TELEGRAM_WEBHOOK_ENABLED:
        logger.info("Webhook enabled")
        app = get_new_configured_app(dispatcher)
        app.on_startup.append(on_startup)
        web.run_app(app, host=settings.TELEGRAM_INTERNAL_HOST, port=settings.TELEGRAM_INTERNAL_PORT)
    else:
        logger.info("Polling enabled")
        executor.start_polling()
