from fastapi_mail import MessageSchema
from passlib.context import CryptContext
import random
import string

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def generate_password() -> str:
    password_length = 12
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ""
    for index in range(password_length):
        password = password + random.choice(characters)
    return str(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
