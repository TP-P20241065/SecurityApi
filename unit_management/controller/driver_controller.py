from typing import Optional, Dict, Any

from fastapi import APIRouter, Path, Body, Query

from shared.response.schema import ResponseSchema
from unit_management.model.driver import CreateDriverModel
from unit_management.service.driver_service import DriverService

router = APIRouter(
    prefix="/driver",
    tags=["driver"],

)


@router.get("", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all_driver():
    result = await DriverService.get_all()
    return result


# Ruta para obtener un driver por ID
@router.get("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_driver_by_id(id: int):
    result = await DriverService.get_by_id(id)
    return result


# Ruta para filtrar drivers
@router.get("/", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_filtered_drivers(name: Optional[str]):
    result = await DriverService.get_filtered(name)
    return result


@router.put("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_driver(driver_id: int = Path(..., alias="id"), *, updateDrive: CreateDriverModel):
    result = await DriverService.update(driver_id, updateDrive)
    return result


@router.delete("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_driver(driver_id: int = Path(..., alias="id")):
    result = await DriverService.delete_by_id(driver_id)
    return result


@router.post("", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_driver(create_data: CreateDriverModel):
    result = await DriverService.create(create_data)
    return result
