from security.service.auth_service import AuthService
from shared.message.message_service import send_email, send_mms
from shared.response.schema import ResponseSchema
from user_management.model.user import CreateUserModelV3, CreateUserModelV2, UserModel
from user_management.repository.user_repository import UserRepository
from fastapi import HTTPException
import asyncio



class UserService:

    @staticmethod
    async def create(data: CreateUserModelV2):

        existing_email, existing_username, existing_dni = await asyncio.gather(
            UserRepository.get_by_email(data.email),
            UserRepository.get_user_by_username(data.username),
            UserRepository.get_user_by_dni(data.dni)
        )

        if existing_email:
            raise HTTPException(status_code=400, detail=f'Correo: {data.email} ya esta registrado')
        if existing_username:
            raise HTTPException(status_code=400, detail=f'Usuario: {data.username} ya esta registrado')
        if existing_dni:
            raise HTTPException(status_code=400, detail=f'DNI: {data.dni} ya esta registrado')

        password = AuthService.generate_password()
        hash_password = AuthService.hash_password(password)
        result = await UserRepository.create(data, hash_password)
        message = send_email(data.email, data.firstName, password)
        await send_mms(message)
        if result:
            return ResponseSchema(detail="Usuario creado exitosamente", result=result)
        else:
            return ResponseSchema(detail="Error al crear usuario!", result=None)

    @staticmethod
    async def create_custom_user(data: CreateUserModelV3):
        existing_email, existing_username, existing_dni = await asyncio.gather(
            UserRepository.get_by_email(data.email),
            UserRepository.get_user_by_username(data.username),
            UserRepository.get_user_by_dni(data.dni)
        )

        if existing_email:
            raise HTTPException(status_code=400, detail=f'Correo: {data.email} ya esta registrado')
        if existing_username:
            raise HTTPException(status_code=400, detail=f'Usuario: {data.username} ya esta registrado')
        if existing_dni:
            raise HTTPException(status_code=400, detail=f'DNI: {data.dni} ya esta registrado')

        # Intentar imprimir data.password para confirmar su disponibilidad
        print(f"Password antes de asignar: {data.password}")  # Debugging line

        # Asignar el valor de password a una variable antes de eliminarlo
        password = data.password
        hash_password = AuthService.hash_password(password)

        # Crear data2 sin el valor de password
        data_dict = data.model_dump()
        data_dict.pop("password")  # Remover el campo de password
        data2 = CreateUserModelV2(**data_dict)

        # Crear usuario
        result = await UserRepository.create(data2, hash_password)

        # Enviar email con la contraseña original
        message = send_email(data.email, data.firstName, password)
        await send_mms(message)

        if result:
            return ResponseSchema(detail="Usuario creado exitosamente", result=result)
        else:
            return ResponseSchema(detail="Error al crear usuario!", result=None)

    @staticmethod
    async def get_all():
        try:
            result = await UserRepository.get_all()
            if result:
                return ResponseSchema(detail="Data successfully obtained!", result=result)
            else:
                ResponseSchema(detail="Data successfully obtained!", result=result)
        except Exception as e:  # Catch any exception
            print(f"Error retrieving user by ID: {e}")  # Log the error
            return ResponseSchema(detail=f"An error occurred: {e}  (esta vacio)", result=None)

    @staticmethod
    async def get_by_id(user_id: int):
        result = await UserRepository.get_by_id(user_id)
        if result:
            return ResponseSchema(detail="Successfully got user by ID!", result=result)
        else:
            return ResponseSchema(detail="Please user id not found.", result=None)

    @staticmethod
    async def get_filtered(isActive: bool):
        try:
            result = await UserRepository.get_filtered(isActive)  # Potential error here
            if result:
                return ResponseSchema(detail="Successfully got user by is active!", result=result)
            else:
                return ResponseSchema(detail="User  not found.", result=None)
        except Exception as e:  # Catch any exception
            print(f"Error retrieving user by is active: {e}")  # Log the error
            return ResponseSchema(detail="An error occurred:", result=None)

    @staticmethod
    async def update(user_id: int, data: CreateUserModelV2):

        # Primero, obtenemos el usuario actual para asegurarnos de que existe
        existing_user = await UserRepository.get_by_id(user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail=f'Usuario con ID {user_id} no encontrado')

            # Comprobamos si hay duplicados en email, username y dni en una sola consulta
        existing_users = await UserRepository.get_users_by_email_username_dni(data.email, data.username, data.dni)

        # Validamos duplicados, ignorando el usuario actual
        for user in existing_users:
            if user.id != user_id:
                if user.email == data.email:
                    raise HTTPException(status_code=400, detail=f'Correo: {data.email} ya está registrado')
                if user.username == data.username:
                    raise HTTPException(status_code=400, detail=f'Usuario: {data.username} ya está registrado')
                if user.dni == data.dni:
                    raise HTTPException(status_code=400, detail=f'DNI: {data.dni} ya está registrado')

        result = await UserRepository.update(user_id, data)
        if result:
            return ResponseSchema(detail="Usuario actualizado exitosamente", result=result)
        else:
            return ResponseSchema(detail="Error al actualizar usuario!", result=None)

    @staticmethod
    async def change_user_password(user_id: int, data: UserModel):
        password = AuthService.generate_password()
        hashed_password = AuthService.hash_password(password)

        try:
            result = await UserRepository.change_password(user_id, hashed_password)
            message = send_email(data.email, data.firstName, password)
            await send_mms(message)
            if result:
                return ResponseSchema(detail="Contaseña restablecida rebice su correo", result=result)
            else:
                return ResponseSchema(detail="Error", result=None)
        except Exception as e:
            print(f"Error updating user by ID: {e}")
            return ResponseSchema(detail=f"An error occurred: {e} : No existe el userId", result=None)

    @staticmethod
    async def delete_by_id(user_id: int):
        result = await UserRepository.delete(user_id)
        if result:
            return ResponseSchema(detail="Usuario eliminado", result=result)
        else:
            return ResponseSchema(detail="User not found.", result=None)
