from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

class CreateUserModelV3(BaseModel):
    username: str
    firstName: str
    lastName: str
    email: str
    headquarter: int
    permissions: List[int]
    dni: str
    password: str
    isActive: bool

class CreateUserModelV2(BaseModel):
    username: str
    firstName: str
    lastName: str
    email: str = Field(default='correo@mail.com')
    headquarter: int
    permissions: List[int]
    dni: str
    isActive: bool


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
    dni: str
    isActive: bool
