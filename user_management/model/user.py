from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class CreateUserModelV2(BaseModel):
    username: str
    firstName: str
    lastName: str
    email: str = Field(default='correo@mail.com')
    headquarter: int
    permissions: List[int]


class UserModel(BaseModel):
    id: int
    createdAt: datetime
    updatedAt: datetime
    username: str
    firstName: str
    lastName: str
    email: str
    headquarter: int
    permissions: List[int]
