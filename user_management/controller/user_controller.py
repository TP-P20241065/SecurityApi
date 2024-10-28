from typing import Optional, Dict, Any, List

from fastapi import APIRouter, Path, Body, Query
from shared.response.schema import ResponseSchema
from user_management.model.user import CreateUserModelV3, CreateUserModelV2, UserModel
from user_management.service.user_service import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"], )


@router.post("", response_model=ResponseSchema[UserModel], response_model_exclude_none=True)
async def create_user(create_data: CreateUserModelV2):
    result = await UserService.create(create_data)
    return result

@router.post("", response_model=ResponseSchema[UserModel], response_model_exclude_none=True)
async def create_custom_user(create_data: CreateUserModelV3):
    result = await UserService.create_custom_user(create_data)
    return result

@router.get("", response_model=ResponseSchema[List[UserModel]], response_model_exclude_none=True)
async def get_all_users():
    result = await UserService.get_all()
    return result


@router.get("/{id}", response_model=ResponseSchema[UserModel], response_model_exclude_none=True)
async def get_user_by_id(id: int):
    result = await UserService.get_by_id(id)
    return result


@router.get("/", response_model=ResponseSchema[List[UserModel]], response_model_exclude_none=True)
async def get_users_is_active(isActive: Optional[bool] = Query(None)):
    result = await UserService.get_filtered(isActive)
    return result


@router.put("/{id}", response_model=ResponseSchema[UserModel], response_model_exclude_none=True)
async def update_user(user_id: int = Path(..., alias="id"), *, updateUser: CreateUserModelV2):
    result = await UserService.update(user_id, updateUser)
    return result

@router.patch("", response_model=ResponseSchema[UserModel], response_model_exclude_none=True)
async def change_user_password(id: int):
    user_data = await get_user_by_id(id)
    result = await UserService.change_user_password(id, user_data.result)
    return result

@router.delete("/{id}", response_model=ResponseSchema[UserModel], response_model_exclude_none=True)
async def delete_user(user_id: int = Path(..., alias="id")):
    result = await UserService.delete_by_id(user_id)
    return result
