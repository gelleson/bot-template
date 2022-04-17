from {{ cookiecutter.project_slug }}.utils.config import get_config, transform_log_level
from {{ cookiecutter.project_slug }}.utils import db, validators

LOG_LEVEL = get_config('LOG_LEVEL', default='INFO', cast=transform_log_level)
LOG_FORMAT = get_config('LOG_FORMAT', default="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s")
LOG_DATE_FORMAT = get_config('LOG_DATE_FORMAT', default="%Y-%m-%d %H:%M:%S")

TELEGRAM_BOT_TOKEN = get_config('TELEGRAM_BOT_TOKEN')
TELEGRAM_WEBHOOK_ENABLED = get_config('TELEGRAM_WEBHOOK_ENABLED', 'false', cast=lambda x: x.lower() == 'true')
TELEGRAM_WEBHOOK_HOST = get_config('TELEGRAM_WEBHOOK_HOST', required=TELEGRAM_WEBHOOK_ENABLED)
TELEGRAM_WEBHOOK_PATH = get_config(
    'TELEGRAM_WEBHOOK_PATH',
    required=TELEGRAM_WEBHOOK_ENABLED,
    validators=[lambda x: x.startswith('/')],
    error_message='Received "{value}", but must be non None and path must start with a slash',
)
TELEGRAM_INTERNAL_HOST = get_config('TELEGRAM_INTERNAL_HOST', default='0.0.0.0')
TELEGRAM_INTERNAL_PORT = get_config('TELEGRAM_INTERNAL_PORT', default=8443, cast=int)
TELEGRAM_WEBHOOK_URL = f"https://{TELEGRAM_WEBHOOK_HOST}{TELEGRAM_WEBHOOK_PATH}"

TELEGRAM_STORAGE = get_config(
    'TELEGRAM_STORAGE',
    default='memory',
    validators=[validators.check_telegram_storage],
    error_message='\"{value}\" is not valid type. Valid types are: memory, redis, mongo'
)

TELEGRAM_STORAGE_REDIS_HOST = get_config(
    'TELEGRAM_STORAGE_REDIS_HOST',
    required=False,
    validators=[validators.check_telegram_redis_host(TELEGRAM_STORAGE == 'redis')],
    error_message='\"{value}\" is not valid host. Valid host is: localhost'
)
TELEGRAM_STORAGE_REDIS_PORT = get_config('TELEGRAM_STORAGE_REDIS_PORT', required=False, default=6379, cast=int)
TELEGRAM_STORAGE_REDIS_DB = get_config('TELEGRAM_STORAGE_REDIS_DB', required=False, default=0, cast=int)
TELEGRAM_STORAGE_REDIS_PASSWORD = get_config('TELEGRAM_STORAGE_REDIS_PASSWORD', required=False)
TELEGRAM_STORAGE_REDIS_POOL_SIZE = get_config('TELEGRAM_STORAGE_REDIS_POOL_SIZE', required=False, default=10, cast=int)
TELEGRAM_STORAGE_REDIS_PREFIX = get_config('TELEGRAM_STORAGE_REDIS_PREFIX', required=False, default="fsm")

DATABASE_CONNECTIONS, DATABASE_DEFAULT, DATABASE_REPLICAS = db.get_databases('DATABASE_URLS')
