import base64
import io
from typing import Optional, Dict, Any

from fastapi import APIRouter, Path, UploadFile, File, Form, HTTPException,Response
from starlette.responses import JSONResponse

from report_management.repository.report_repository import ReportRepository
from shared.message.message_service import send_alert, send_mms
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
        incident: Optional[str] = Form(None),
        tracking_link: str = Form(...),
        image: UploadFile = File(...),
        unit_id: int = Form(...)
):
    # Lee los datos de la imagen
    image_data = await image.read()

    # Crea un flujo de bytes para la imagen
    image_attachment = io.BytesIO(image_data)
    image_attachment.name = image.filename  # Establece el nombre del archivo

    # Crea un nuevo UploadFile temporal para pasar a send_alert
    temp_upload_file = UploadFile(
        filename=image_attachment.name,
        file=image_attachment
    )

    # Pasa el UploadFile temporal a send_alert
    message = await send_alert(address, incident, tracking_link, temp_upload_file, unit_id)

    try:
        await send_mms(message)
    except Exception:
        raise HTTPException(status_code=400, detail='Ocurrió un error del remitente al intentar enviar el reporte.')

    # Usa image_data para crear el reporte
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