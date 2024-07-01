

from shared.message.message_service import send_email, send_mms
from shared.response.schema import ResponseSchema
from user_management.model.user import CreateUserModelV2
from user_management.repository.user_repository import UserRepository
from security.service.security_service import generate_password


class UserService:


    @staticmethod
    async def create(data: CreateUserModelV2):
        password = generate_password()
        result = await UserRepository.create(data, password)
        message = send_email(data.email, data.email, password)
        await send_mms(message)
        if result:
            return ResponseSchema(detail="Successfully create user!", result=result)
        else:
            return ResponseSchema(detail="Failed to create user!", result=None)

    @staticmethod
    async def get_all():
        try:
            result = await UserRepository.get_all()
            if result:
                return ResponseSchema(detail="Successfully get all data!", result=result)
            else:
                ResponseSchema(detail="Please get all data not found!", result=result)
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
        try:
            result = await UserRepository.update(user_id, data)
            if result:
                return ResponseSchema(detail="Successfully update user!", result=result)
            else:
                return ResponseSchema(detail="user not found.", result=None)
        except Exception as e:
            print(f"Error updating user by ID: {e}")
            return ResponseSchema(detail=f"An error occurred: {e} : no existe el userId", result=None)

    @staticmethod
    async def delete_by_id(user_id: int):
        result = await UserRepository.delete(user_id)
        if result:
            return ResponseSchema(detail="Successfully delete user!", result=result)
        else:
            return ResponseSchema(detail="User not found.", result=None)