from pydantic import Field, EmailStr, validator
from typing import List

from shared.domain.base_domain import BaseDomain


class User(BaseDomain):
    id: int
    username: str
    firstName: str
    lastName: str
    email: EmailStr
    headquarter: int
    permissions: List[int]
    is_active: bool = Field(default=True)

    @validator('username')
    def validate_username(cls, value):
        if not value:
            raise ValueError('El nombre de usuario no puede estar vacío')
        return value

    @validator('email')
    def validate_email(cls, value):
        if "@" not in value:
            raise ValueError('Email inválido')
        return value
