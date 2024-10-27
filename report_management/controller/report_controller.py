import base64
from typing import Optional, Dict, Any

from fastapi import APIRouter, Path, UploadFile, File, Form, HTTPException,Response
from starlette.responses import JSONResponse

from report_management.repository.report_repository import ReportRepository
from shared.response.schema import ResponseSchema, ResponseSchema2
from report_management.model.report import  ReportCreate
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
async def get_filtered_reports(incident: Optional[str]):
    result = await ReportService.get_filtered(incident)
    return result


@router.put("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_report(camera_id: int = Path(..., alias="id"), *, updateCamera: ReportCreate):
    result = await ReportService.update(camera_id, updateCamera)
    return result


@router.delete("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_report(camera_id: int = Path(..., alias="id")):
    result = await ReportService.delete_by_id(camera_id)
    return result


@router.post("/upload/")
async def create_report(
    address: str = Form(...),
    incident: str = Form(...),
    tracking_link: str = Form(...),
    image: UploadFile = File(...),
    unit_id: int = Form(...)
):
    image_data = await image.read()
    report = await ReportService.create_report(address, incident, tracking_link, image_data, unit_id)
    if not report:
        raise HTTPException(status_code=400, detail="Error al crear reporte")
    return {"id": report.id}


@router.get("/report/{report_id}/image")
async def fetch_report_image(report_id: int):
    image_base64 = await ReportService.get_report_image(report_id)
    if image_base64:
        return JSONResponse(content={"image": image_base64})
    else:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")