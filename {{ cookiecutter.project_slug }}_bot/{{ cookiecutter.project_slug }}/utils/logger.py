import sys
import logging
from {{ cookiecutter.project_slug }} import settings


def install():
    fmt = logging.Formatter(
        fmt=settings.LOG_FORMAT,
        datefmt=settings.LOG_DATE_FORMAT,
    )
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(settings.LOG_LEVEL)
    sh.setFormatter(fmt)
    logger = logging.getLogger(__name__)
    logger.setLevel(settings.LOG_LEVEL)
    logger.addHandler(sh)

    # will print debug sql
    logger_db_client = logging.getLogger("db_client")
    logger_db_client.setLevel(settings.LOG_LEVEL)
    logger_db_client.addHandler(sh)

    logger_tortoise = logging.getLogger("tortoise")
    logger_tortoise.setLevel(settings.LOG_LEVEL)
    logger_tortoise.addHandler(sh)
