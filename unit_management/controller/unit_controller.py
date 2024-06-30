from typing import Optional, Dict, Any

from fastapi import APIRouter, Path, Body, Query
from shared.response.schema import ResponseSchema
from unit_management.model.unit import CreateUnitModel
from unit_management.service.unit_service import UnitService

router = APIRouter(
    prefix="/unit",
    tags=["unit"], )


@router.get("", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all_unit():
    result = await UnitService.get_all()
    return result


# Ruta para obtener un driver por ID
@router.get("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_unit_by_id(id: int):
    result = await UnitService.get_by_id(id)
    return result


# Ruta para filtrar drivers
@router.get("/", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_filtered_units(name: Optional[str]):
    result = await UnitService.get_filtered(name)
    return result


@router.put("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_unit(driver_id: int = Path(..., alias="id"), *, updateUnit: CreateUnitModel):
    result = await UnitService.update(driver_id, updateUnit)
    return result


@router.delete("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_unit(unit_id: int = Path(..., alias="id")):
    result = await UnitService.delete_by_id(unit_id)
    return result


@router.post("", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_driver(create_data: CreateUnitModel):
    result = await UnitService.create(create_data)
    return result
