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
    # Verificar si el usuario existe
    if await AuthService.user_existed(login.email):
        user = await AuthService.get_user(login.email)
        # Verificar si la cuenta está activa
        if user.isActive:
            # Verificar si la contraseña es correcta
            if AuthService.verify_password(login.password, user.hashedPassword):
                token = await AuthService.create_access_token(user)
                return token
            else:
                # Contraseña incorrecta
                raise HTTPException(status_code=400, detail="Password or email incorrect")
        else:
            # Usuario inactivo
            raise HTTPException(status_code=400, detail="The account is deactivated")
    else:
        # Correo electrónico no registrado
        raise HTTPException(status_code=400, detail="Email not registered")



@router.patch("/reset-password", response_model=ResponseSchema)
async def reset_password(email: str):
    if await AuthService.user_existed(email):
        result = await AuthService.change_password_by_email(email)
        return result
    else:
        raise HTTPException(status_code=400, detail="Email not existed")
