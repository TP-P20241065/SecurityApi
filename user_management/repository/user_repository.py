import json

from config.connection import prisma_connection
from user_management.model.user import CreateUserModelV2


class UserRepository:

    @staticmethod
    async def create(user: CreateUserModelV2, password: str):
        return await prisma_connection.prisma.user.create({
            'username': user.username,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'email': user.email,
            'headquarter': user.headquarter,
            'permissions': json.dumps(user.permissions),
            'hashedPassword': password,
            'dni': user.dni
        })

    @staticmethod
    async def get_all():
        try:
            return await prisma_connection.prisma.user.find_many()
        except Exception as e:
            print(f"Error retrieving user by ID: {e}")

    @staticmethod
    async def get_by_id(user_id: int):
        return await prisma_connection.prisma.user.find_first(where={"id": user_id})

    @staticmethod
    async def get_by_email(email: str):
        return await prisma_connection.prisma.user.find_first(where={"email": email})

    @staticmethod
    async def get_users_by_email_username_dni(email: str, username: str, dni: str):
        return await prisma_connection.prisma.user.find_many(
            where={
                "OR": [
                    {"email": email},
                    {"username": username},
                    {"dni": dni}
                ]
            }
        )

    @staticmethod
    async def get_user_by_dni(dni: int):
        return await prisma_connection.prisma.user.find_first(where={"dni": dni})

    @staticmethod
    async def get_user_by_username(username: str):
        return await prisma_connection.prisma.user.find_first(where={"username": username})

    @staticmethod
    async def get_filtered(isActive: bool):
        record = await prisma_connection.prisma.user.find_many(where={"isActive": isActive})
        # print(f"Record retrieved: {record}")  # Add console logging with f-string
        return record

    @staticmethod
    async def update(user_id: int, user: CreateUserModelV2):
        return await prisma_connection.prisma.user.update(where={"id": user_id}, data={
            'username': user.username,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'email': user.email,
            'headquarter': user.headquarter,
            'permissions': json.dumps(user.permissions),
            'dni': user.dni,
            'isActive': user.isActive
        })

    @staticmethod
    async def change_password(user_id: int, password: str):
        return await prisma_connection.prisma.user.update(where={"id": user_id}, data={
            'hashedPassword': password
        })

    @staticmethod
    async def delete(user_id: int):
        return await prisma_connection.prisma.user.delete(where={"id": user_id})

    @staticmethod
    async def get_user(email: str):
        result = await prisma_connection.prisma.user.find_first(where={"email": email})
        # print(f"Record retrieved: {record}")  # Add console logging with f-string
        return result



