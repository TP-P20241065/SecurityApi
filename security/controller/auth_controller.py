from fastapi import APIRouter, Path, Body, Query, HTTPException

from security.model.auth import Register, DataToken, TokenModel
from security.service.auth_service import AuthService
from shared.response.schema import ResponseSchema

router = APIRouter(
    prefix="/auth",
    tags=["Security"], )


@router.post("/register", response_model=ResponseSchema)
async def register(register: Register):
    result = AuthService.hash_password(register.password)
    return ResponseSchema(detail="hashed created!", result=result)


@router.post("/login", response_model=TokenModel)
async def login(login: Register):
    if await AuthService.user_existed(login.email):
        user = await AuthService.get_user(login.email)
        if AuthService.verify_password(login.password, user.hashedPassword):
            token = await AuthService.create_access_token(user)
            return token
        else:
            raise HTTPException(status_code=401, detail="Contraseña o Correo electrónico incorrecta")
    else:
        raise HTTPException(status_code=401, detail="Correo electrónico no registrado")


@router.patch("/reset-password", response_model=ResponseSchema)
async def reset_password(email: str):
    if await AuthService.user_existed(email):
        result = await AuthService.change_password_by_email(email)
        return result
    else:
        return ResponseSchema(details="Email not existed", result=None)
