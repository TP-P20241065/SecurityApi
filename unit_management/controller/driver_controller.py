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
    return ResponseSchema(detail="Successfully get all data!", result=result)


# Ruta para obtener un driver por ID
@router.get("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_driver_by_id(id: int):
    result = await DriverService.get_by_id(id)
    return ResponseSchema(detail="Successfully got driver by ID!", result=result)


# Ruta para filtrar drivers
@router.get("/", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_filtered_drivers(name: Optional[str]):
    if name:
        result = await DriverService.get_filtered(name)
        return ResponseSchema(detail="Successfully got filtered data!", result=result)
    else:
        return ResponseSchema(detail="Please provide attributes for search.", result=None)


@router.put("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_driver(driver_id: int = Path(..., alias="id"), *, updateDrive: CreateDriverModel):
    result = await DriverService.update(driver_id, updateDrive)
    return ResponseSchema(detail="Successfully update driver!", result=result)


@router.delete("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_driver(driver_id: int = Path(..., alias="id")):
    result = await DriverService.delete_by_id(driver_id)
    return ResponseSchema(detail="Successfully delete driver!", result=result)


@router.post("", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_driver(create_data: CreateDriverModel):
    result = await DriverService.create(create_data)
    return ResponseSchema(detail="Successfully create driver!", result=result)
