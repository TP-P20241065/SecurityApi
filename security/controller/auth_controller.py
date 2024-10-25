from fastapi import APIRouter, Path, Body, Query, HTTPException, Depends

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


@router.post("/login/portal-desktop", response_model=TokenModel)
async def login_portal_desktop(login: Register):
    # Verificar si el usuario existe
    if await AuthService.user_existed(login.email):
        user = await AuthService.get_user(login.email)
        # Verificar si la cuenta está activa
        if user.isActive:
            if 2 in user.permissions:
                if AuthService.verify_password(login.password, user.hashedPassword):
                    token = await AuthService.create_access_token(user)
                    return token
                else:
                    # Contraseña incorrecta
                    raise HTTPException(status_code=400, detail="Password or email incorrect")
            else:
                # Usuario no tiene permiso para acceder al aplicacion de escritorio
                raise HTTPException(status_code=400,
                                    detail="No tienes permiso para acceder la aplicación de escritorio.")
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


@router.post("/login/portal-admin", response_model=TokenModel)
async def login_portal_admin(login: Register):
    # Verificar si el usuario existe
    if await AuthService.user_existed(login.email):
        user = await AuthService.get_user(login.email)
        # Verificar si la cuenta está activa
        if user.isActive:
            if 0 in user.permissions or 1 in user.permissions:
                if AuthService.verify_password(login.password, user.hashedPassword):
                    token = await AuthService.create_access_token(user)
                    return token
                else:
                    # Contraseña incorrecta
                    raise HTTPException(status_code=400, detail="Password or email incorrect")
            else:
                # Usuario no tiene permiso para acceder al portal administrativo
                raise HTTPException(status_code=400,
                                    detail="No tienes permiso para acceder al portal administrativo.")
            # Verificar si la contraseña es correcta

        else:
            # Usuario inactivo
            raise HTTPException(status_code=400, detail="The account is deactivated")
    else:
        # Correo electrónico no registrado
        raise HTTPException(status_code=400, detail="Email not registered")
