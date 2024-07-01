import json

from config.connection import prisma_connection
from user_management.model.user import CreateUserModelV2


class UserRepository:

    @staticmethod
    async def create(user: CreateUserModelV2, password: str):
        print(f"password 2 : {password}")
        return await prisma_connection.prisma.user.create({
            'username': user.username,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'email': user.email,
            'headquarter': user.headquarter,
            'permissions': json.dumps(user.permissions),
            'hashedPassword': password
        })

    @staticmethod
    async def get_all():
        return await prisma_connection.prisma.user.find_many()

    @staticmethod
    async def get_by_id(user_id: int):
        return await prisma_connection.prisma.user.find_first(where={"id": user_id})

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
            'permissions': json.dumps(user.permissions)
        })

    @staticmethod
    async def delete(user_id: int):
        return await prisma_connection.prisma.user.delete(where={"id": user_id})
