from typing import Optional, Dict, Any

from fastapi import APIRouter, Path, Body, Query
from shared.response.schema import ResponseSchema
from unit_management.model.camera import CreateCameraModel
from unit_management.service.camera_service import CameraService

router = APIRouter(
    prefix="/camera",
    tags=["camera"], )


@router.get("", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all_camera():
    result = await CameraService.get_all()
    return result


# Ruta para obtener un driver por ID
@router.get("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_camera_by_id(id: int):
    result = await CameraService.get_by_id(id)
    return result


# Ruta para filtrar drivers
@router.get("/", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_filtered_cameras(name: Optional[str]):
    result = await CameraService.get_filtered(name)
    return result


@router.put("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_camera(camera_id: int = Path(..., alias="id"), *, updateCamera: CreateCameraModel):
    result = await CameraService.update(camera_id, updateCamera)
    return result


@router.delete("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_camera(camera_id: int = Path(..., alias="id")):
    result = await CameraService.delete_by_id(camera_id)
    return result


@router.post("", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_camera(create_data: CreateCameraModel):
    result = await CameraService.create(create_data)
    return result
