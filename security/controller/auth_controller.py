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
    if not await AuthService.user_existed(login.email):
        # Correo electrónico no registrado
        raise HTTPException(status_code=400, detail="Correo no registrado")

    user = await AuthService.get_user(login.email)

    # Verificar si la contraseña es correcta
    if not AuthService.verify_password(login.password, user.hashedPassword):
        # Contraseña incorrecta
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    # Verificar si la cuenta está activa
    if not user.isActive:
        # Usuario inactivo
        raise HTTPException(status_code=400, detail="La cuenta está desactivada")

    # Verificar si la cuenta tiene permiso para acceder a la aplicación de escritorio
    if 0 not in user.permissions and 2 not in user.permissions:
        raise HTTPException(status_code=400,
                            detail="No tienes permiso para acceder a la aplicación de escritorio.")

    # Crear y retornar el token de acceso si todas las verificaciones pasan
    token = await AuthService.create_access_token(user)
    return token


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
    if not await AuthService.user_existed(login.email):
        # Correo electrónico no registrado
        raise HTTPException(status_code=400, detail="Correo no registrado")

    user = await AuthService.get_user(login.email)

    # Verificar si la contraseña es correcta
    if not AuthService.verify_password(login.password, user.hashedPassword):
        # Contraseña incorrecta
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    # Verificar si la cuenta está activa
    if not user.isActive:
        # Usuario inactivo
        raise HTTPException(status_code=400, detail="La cuenta está desactivada")

    # Verificar si la cuenta tiene permiso para acceder al portal administrativo
    if 0 not in user.permissions and 1 not in user.permissions:
        raise HTTPException(status_code=400,
                            detail="No tienes permiso para acceder al portal administrativo.")

    # Crear y retornar el token de acceso si todas las verificaciones pasan
    token = await AuthService.create_access_token(user)
    return token

