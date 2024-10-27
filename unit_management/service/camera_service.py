from fastapi import HTTPException

from shared.exception.validators import validate_existence, validate_uniqueness, validate_uniqueness_by_id
from shared.response.schema import ResponseSchema
from unit_management.model.camera import CreateCameraModel
from unit_management.repository.camera_repository import CameraRepository


class CameraService:

    @staticmethod
    async def get_all():
        try:
            result = await CameraRepository.get_all()
            if result:
                return ResponseSchema(detail="Data successfully obtained!", result=result)
            else:
                ResponseSchema(detail="Data successfully obtained!", result=result)
        except Exception as e:  # Catch any exception
            print(f"Error retrieving camera by ID: {e}")  # Log the error
            return ResponseSchema(detail=f"An error occurred: {e}  (esta vacio)", result=None)

    @staticmethod
    async def get_by_id(camera_id: int):
        result = await CameraRepository.get_by_id(camera_id)
        if result:
            return ResponseSchema(detail="Successfully got camera by ID!", result=result)
        else:
            return ResponseSchema(detail="Please camera id not found.", result=None)

    # es un ejemplo para ver los errores en consola si es que hay
    @staticmethod
    async def get_filtered(name: str):
        try:
            result = await CameraRepository.get_filtered(name)  # Potential error here
            if result:
                return ResponseSchema(detail="Successfully got camera by unit!", result=result)
            else:
                return ResponseSchema(detail="Camera name not found.", result=None)
        except Exception as e:  # Catch any exception
            print(f"Error retrieving camera by ID: {e}")  # Log the error
            return ResponseSchema(detail="An error occurred:", result=None)

    @staticmethod
    async def create(data: CreateCameraModel):
        existing_item_duplicate = await CameraRepository.get_cameras_by_name_url(data.name, data.url)
        attributes_to_check = {
            'name': data.name,
            'url': data.url,
            # Puedes agregar más atributos aquí
        }
        validate_uniqueness(existing_item_duplicate, attributes_to_check)
        result = await CameraRepository.create(data)
        if result:
            return ResponseSchema(detail="Camara creada!", result=result)
        else:
            raise HTTPException(status_code=500, detail="Error al crear camara")

    @staticmethod
    async def update(camera_id: int, data: CreateCameraModel):
        # valida si existe el objeto y da las respuesta correspondiente
        existing_item = await CameraRepository.get_by_id(camera_id)
        validate_existence(existing_item, camera_id, "Camara")
        # valida si ya existen objetos con atributos duplicados
        existing_item_duplicate = await CameraRepository.get_cameras_by_name_url(data.name, data.url)
        attributes_to_check = {
            'name': data.name,
            'url': data.url,
            # Puedes agregar más atributos aquí
        }
        validate_uniqueness_by_id(existing_item_duplicate, camera_id, attributes_to_check)
        result = await CameraRepository.update(camera_id, data)
        if result:
            return ResponseSchema(detail="Camara actualizada exitosamente", result=result)
        else:
            raise HTTPException(status_code=500, detail="Error al actualizar unidad!")


    @staticmethod
    async def delete_by_id(camera_id: int):
        result = await CameraRepository.delete(camera_id)
        if result:
            return ResponseSchema(detail="Camara eliminada!", result=result)
        else:
            return ResponseSchema(detail="Camera not found.", result=None)
