from enum import Enum
from tortoise import Model, fields


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=250)
    full_name = fields.CharField(max_length=250)
    last_action = fields.DatetimeField(auto_now_add=True)
    language = fields.CharField(max_length=10)
    is_active = fields.BooleanField(default=True)
    role = fields.CharEnumField(Role, default=Role.USER)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"
