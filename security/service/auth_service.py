import string
import random
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

from security.model.auth import DataToken, TokenModel
from shared.message.message_service import send_email, send_mms
from shared.response.schema import ResponseSchema
from user_management.repository.user_repository import UserRepository


class AuthService:
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
    secret_key = "tu_clave_secreta_aqui"  # Deberías manejar la clave secreta de forma segura en un entorno real

    @staticmethod
    def hash_password(password: str) -> str:
        return AuthService.pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return AuthService.pwd_context.verify(password, hashed_password)

    @staticmethod
    def generate_password() -> str:
        password_length = 12
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ""
        for index in range(password_length):
            password = password + random.choice(characters)
        return str(password)

    @staticmethod
    async def create_access_token(data: any, expires_delta: timedelta = None) -> TokenModel:
        new_token_data = DataToken(
            username=data.username,
            firstName=data.firstName,
            lastName=data.lastName,
            email=data.email,
            permissions=data.permissions,
            isActive=data.isActive,
        )
        token = new_token_data.dict()
        to_encode = token.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=25)  # Ejemplo de expiración corta por defecto
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, AuthService.secret_key, algorithm="HS256")
        return TokenModel(access_token=encoded_jwt, token_type="bearer")

    @staticmethod
    async def decode_access_token(token: str) -> dict:
        try:
            decoded_token = jwt.decode(token, AuthService.secret_key, algorithms=["HS256"])
            return decoded_token
        except jwt.ExpiredSignatureError:
            # Manejar token expirado
            return None
        except jwt.InvalidTokenError:
            # Manejar token inválido
            return None

    @staticmethod
    async def user_existed(email: str) -> bool:
        result = await UserRepository.get_user(email)
        return bool(result)

    @staticmethod
    async def get_user(email: str):
        result = await UserRepository.get_user(email)
        return result

    @staticmethod
    async def change_password_by_email(email: str):
        try:
            password = AuthService.generate_password()
            hashed_password = AuthService.hash_password(password)
            user = await UserRepository.get_user(email)
            result = await UserRepository.change_password(email, hashed_password)
            if result:
                message = send_email(user.email, user.firstName, password)
                await send_mms(message)
                return ResponseSchema(detail="Successfully!", result=result)
            else:
                return ResponseSchema(detail="Not change password", result=None)
        except Exception as e:
            print(f"Error change password: {e}")
            return ResponseSchema(detail=f"An error occurred: {e} : authService", result=None)
