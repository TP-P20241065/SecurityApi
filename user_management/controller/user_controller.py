from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND

from user_management.domain.user import User
from user_management.resource.new_user import NewUserResource

# Ejemplos de usuarios en formato JSON
example_users = [
    {
        "id": 1,
        "username": "john_doe",
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "headquarter": 123,
        "permissions": [1, 2, 3],
        "is_active": True,
        "created_at": "2024-06-29T15:30:00Z",
        "updated_at": "2024-06-29T15:30:00Z"
    },
    {
        "id": 2,
        "username": "marco_bka",
        "firstName": "Marco",
        "lastName": "Bka",
        "email": "marco.bka@example.com",
        "headquarter": 123,
        "permissions": [1, 2, 3],
        "is_active": True,
        "created_at": "2024-06-29T15:30:00Z",
        "updated_at": "2024-06-29T15:30:00Z"
    }
]

# Lista de usuarios inicial vacía
users = example_users.copy()

class UserController:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/users/", self.create_user, methods=["POST"])
        """self.router.add_api_route("/users/{user_id}", self.get_user, methods=["GET"])
        self.router.add_api_route("/users/", self.get_all_users, methods=["GET"])
        self.router.add_api_route("/users/{user_id}", self.update_user, methods=["PUT"])
        self.router.add_api_route("/users/{user_id}", self.delete_user, methods=["DELETE"]) """

    async def create_user(self, user: NewUserResource):
        new_user = User(
            id=len(users) + 1,
            username=user.username,
            firstName=user.firstName,
            lastName=user.lastName,
            email=user.email,
            headquarter=user.headquarter,
            permissions=user.permissions,
            is_active=user.is_active
        )

        example_users.append(new_user.dict())
        return example_users


