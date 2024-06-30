from typing import List

from pydantic import BaseModel, EmailStr


class CreateUserModel(BaseModel):
    userName: str
    firsName: str
    lastName: int
    email: EmailStr
    headquarter: str
    permissions: List[int]


class UserModel(BaseModel):
    id: int
    userName: str
    firsName: str
    lastName: int
    email: EmailStr
    headquarter: str
    permissions: List[int]
