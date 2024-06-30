from dataclasses import Field
from typing import List
from pydantic import EmailStr, BaseModel, validator


class UpdateUserResource(BaseModel):
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
        # Pydantic ya valida los emails, pero puedes agregar reglas adicionales aquí
        if "@" not in value:
            raise ValueError('Email inválido')
        return value