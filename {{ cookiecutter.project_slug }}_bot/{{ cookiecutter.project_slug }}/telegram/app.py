from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from {{ cookiecutter.project_slug }} import settings

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)


def get_storage():
    match settings.TELEGRAM_STORAGE:
        case 'memory':
            return MemoryStorage()
        case 'redis':
            return RedisStorage2(
                host=settings.TELEGRAM_STORAGE_REDIS_HOST,
                port=settings.TELEGRAM_STORAGE_REDIS_PORT,
                db=settings.TELEGRAM_STORAGE_REDIS_DB,
                password=settings.TELEGRAM_STORAGE_REDIS_PASSWORD,
                pool_size=settings.TELEGRAM_STORAGE_REDIS_POOL_SIZE,
                prefix=settings.TELEGRAM_STORAGE_REDIS_PREFIX,
            )
        case _:
            raise ValueError(f'Unknown storage {settings.TELEGRAM_STORAGE}')


storage = get_storage()

dispatcher = Dispatcher(bot, storage=storage)
