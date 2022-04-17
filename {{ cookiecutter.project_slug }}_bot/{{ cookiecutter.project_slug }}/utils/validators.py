def check_telegram_storage(storage: str) -> bool:
    return storage in ['memory', 'redis']


def check_telegram_redis_host(storage_enabled: bool):
    def return_true(value: str) -> bool:
        return True

    if not storage_enabled:
        return return_true

    def check_host(host: str) -> bool:
        return storage_enabled and host is not None

    return check_host
