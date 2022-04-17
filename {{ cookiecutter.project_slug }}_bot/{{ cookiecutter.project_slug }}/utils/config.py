from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from os import getenv
from typing import TypeVar, Callable, List
import logging


logger = logging.getLogger("config")

T = TypeVar('T')


def get_config(
        key: str,
        default: T = None,
        required=True,
        cast: Callable[[str], T | List[T]] | None = None,
        validators: List[Callable[[T], bool]] = None,
        factory: Callable[[], T] = None,
        error_message: str | None = None,
) -> T | None:
    value = getenv(key, default)

    if required and value is None:
        if error_message is not None:
            raise ValueError(error_message.format(key=key))
        else:
            raise ValueError(f'Missing required environment variable: {key}')

    if cast is not None:
        value = cast(value)

    if factory is not None and value is None:
        logging.warning(f'Using factory for {key}')
        value = factory()

    if validators is not None and value is not None:
        for validator in validators:
            if not validator(value):
                if error_message is None:
                    raise ValueError(f'Invalid value for {key}: {value}')
                else:
                    raise ValueError(error_message.format(key=key, value=value))

    return value


def transform_log_level(log_level: str) -> int:
    log_level = log_level.upper()
    if log_level == 'DEBUG':
        return logging.DEBUG
    elif log_level == 'INFO':
        return logging.INFO
    elif log_level == 'WARNING':
        return logging.WARNING
    elif log_level == 'ERROR':
        return logging.ERROR
    elif log_level == 'CRITICAL':
        return logging.CRITICAL
    else:
        raise ValueError(f'Invalid log level: {log_level}')
