from os import getenv, environ

__config = None
__default = None
__replicas = None


def get_databases(key: str):
    global __config, __default, __replicas
    if __config is None:
        __config, __default, __replicas = _get_databases(key)
    return __config, __default, __replicas


def _get_databases(key: str):
    databases = getenv(key, None)

    if databases is None:
        raise ValueError(f"DATABASE_URLS is not set")

    databases = databases.split(",")

    config = {}
    config['default'] = databases[0]
    replicas = []

    if len(databases) > 1:
        for index, database in enumerate(databases[1:]):
            config[f"replica_{index}"] = database
            replicas.append((f"replica_{index}", database))

    return config, config['default'], replicas
