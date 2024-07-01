from typing import List

from pydantic import BaseModel


class Register(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    hashedPassword: str


class TokenModel(BaseModel):
    access_token: str
    token_type: str


class DataToken(BaseModel):
    username: str
    firstName: str
    lastName: str
    email: str
    permissions: List[int]
    isActive: bool

