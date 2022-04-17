from typing import Type, List

from tortoise import Model
from {{cookiecutter.project_slug}} import settings
from random import choice


class Router:
    primary: str
    replicas: List[str] = []

    def __init__(self):
        self.primary = 'default'

        replicas = dict(**settings.DATABASE_CONNECTIONS)
        replicas.pop('default')
        self.replicas = [x for x in replicas.keys()] if len(replicas) > 0 else []

    def db_for_read(self, model: Type[Model]):
        if len(self.replicas) == 0:
            return 'default'

        return choice(self.replicas)

    def db_for_write(self, model: Type[Model]):
        return self.primary
