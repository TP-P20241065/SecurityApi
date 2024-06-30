from shared.response.schema import ResponseSchema
from unit_management.model.camera import CreateCameraModel
from unit_management.repository.camera_repository import CameraRepository


class UnitService:

    @staticmethod
    async def get_all():
        result = await CameraRepository.get_all()
        if result:
            return ResponseSchema(detail="Successfully get all data!", result=result)
        else:
            ResponseSchema(detail="Please get all data not found!", result=result)

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
        result = await CameraRepository.create(data)
        if result:
            return ResponseSchema(detail="Successfully create camera!", result=result)
        else:
            return ResponseSchema(detail="Failed to create camera!", result=None)

    @staticmethod
    async def update(camera_id: int, data: CreateCameraModel):
        try:
            result = await CameraRepository.update(camera_id, data)
            if result:
                return ResponseSchema(detail="Successfully update camera!", result=result)
            else:
                return ResponseSchema(detail="Camera not found.", result=None)
        except Exception as e:
            print(f"Error updating unit by ID: {e}")
            return ResponseSchema(detail=f"An error occurred: {e} : no existe el unitId", result=None)

    @staticmethod
    async def delete_by_id(camera_id: int):
        result = await CameraRepository.delete(camera_id)
        if result:
            return ResponseSchema(detail="Successfully delete camera!", result=result)
        else:
            return ResponseSchema(detail="Camera not found.", result=None)
