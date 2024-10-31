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
from unit_management.controller.camera_controller import get_all_camera
import cv2
import yt_dlp as youtube_dl

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
        image: UploadFile = File(None),
        unit_id: int = Form(...)
):
    def youtube_stream(current_view):
        youtube_url = current_view

        # Configuración para seleccionar la calidad en 480p o la mejor calidad inferior disponible
        ydl_opts = {
            'format': 'best[height<=480]/best',  # 480p o la mejor calidad inferior posible
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            live_url = info['url']

        return cv2.VideoCapture(live_url)

    def ip_stream(current_view):
        return cv2.VideoCapture(current_view)

    def link_check(current_view):
        if current_view == '0':
            return cv2.VideoCapture(0)
        elif 'youtube.com' in current_view or 'youtu.be' in current_view:
            return youtube_stream(current_view)
        else:
            return ip_stream(current_view)

    if not image:
        response = await get_all_camera()
        cameras = response.result if response.detail == 'Data successfully obtained!' else []

        # Filtrar y obtener los unitId de cámaras
        unit_cameras = list(
            {camera.url for camera in cameras if camera.unitId == unit_id}
        )

        print("Url listed")
        # Capturar la transmisión de video
        cap = link_check(unit_cameras[0])
        ret, frame = cap.read()  # Leer el fotograma de la cámara
        cap.release()

        print("Ret")
        # Verificar si se capturó el fotograma correctamente
        if not ret:
            raise HTTPException(status_code=400, detail="No se pudo capturar la imagen desde la transmisión.")

        print("Convertir")
        # Convertir el fotograma al formato RGB y guardarlo en un archivo temporal en memoria
        _, buffer = cv2.imencode('.jpg', frame)
        image_data = io.BytesIO(buffer.tobytes())
        image_data.name = "boton_panico.jpg"

        print("Boton panico")

        # Crear un objeto UploadFile desde el archivo en memoria
        image = UploadFile(
            filename=image_data.name,
            file=image_data
        )

    print("Imagen data")
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