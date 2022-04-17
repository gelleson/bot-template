from {{ cookiecutter.project_slug }} import settings

TORTOISE_ORM = {
    "connections": settings.DATABASE_CONNECTIONS,
    "apps": {
        "models": {
            "models": ["{{ cookiecutter.project_slug }}.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": True,
    "routers": ["{{ cookiecutter.project_slug }}.db.router.Router"],
}
