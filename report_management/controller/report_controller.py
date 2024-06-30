from typing import Optional, Dict, Any

from fastapi import APIRouter, Path, Body, Query
from shared.response.schema import ResponseSchema
from report_management.model.report import CreateReportModel
from report_management.service.report_service import ReportService

router = APIRouter(
    prefix="/report",
    tags=["report"], )


@router.get("", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all_report():
    result = await ReportService.get_all()
    return result


# Ruta para obtener un driver por ID
@router.get("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_report_by_id(id: int):
    result = await ReportService.get_by_id(id)
    return result


# Ruta para filtrar drivers
@router.get("/", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_filtered_reports(name: Optional[str]):
    result = await ReportService.get_filtered(name)
    return result


@router.put("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_report(camera_id: int = Path(..., alias="id"), *, updateCamera: CreateReportModel):
    result = await ReportService.update(camera_id, updateCamera)
    return result


@router.delete("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_report(camera_id: int = Path(..., alias="id")):
    result = await ReportService.delete_by_id(camera_id)
    return result


@router.post("", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_report(create_data: CreateReportModel):
    result = await ReportService.create(create_data)
    return result
