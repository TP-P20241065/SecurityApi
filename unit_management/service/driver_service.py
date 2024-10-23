from typing import Dict

from shared.response.schema import ResponseSchema
from unit_management.model.driver import CreateDriverModel
from unit_management.repository.driver_repository import DriverRepository


class DriverService:

    @staticmethod
    async def get_all():
        result = await DriverRepository.get_all()
        if result:
            return ResponseSchema(detail="Data successfully obtained!", result=result)
        else:
            ResponseSchema(detail="Data successfully obtained!", result=result)

    @staticmethod
    async def get_by_id(driver_id: int):
        result = await DriverRepository.get_by_id(driver_id)
        if result:
            return ResponseSchema(detail="Successfully got driver by ID!", result=result)
        else:
            return ResponseSchema(detail="Please driver id not found.", result=None)

    # es un ejemplo para ver los errores en consola si es que hay
    @staticmethod
    async def get_filtered(name: str):
        try:
            result = await DriverRepository.get_filtered(name)  # Potential error here
            if result:
                return ResponseSchema(detail="Successfully got driver by name!", result=result)
            else:
                return ResponseSchema(detail="Driver name not found.", result=None)
        except Exception as e:  # Catch any exception
            print(f"Error retrieving driver by ID: {e}")  # Log the error
            return ResponseSchema(detail="An error occurred:", result=None)

    @staticmethod
    async def create(data: CreateDriverModel):
        result = await DriverRepository.create(data)
        if result:
            return ResponseSchema(detail="Conductor creado exitosamente", result=result)
        else:
            return ResponseSchema(detail="Error al crear conductor!", result=None)

    @staticmethod
    async def update(driver_id: int, data: CreateDriverModel):
        try:
            result = await DriverRepository.update(driver_id, data)
            if result:
                return ResponseSchema(detail="Conductor actualizado", result=result)
            else:
                return ResponseSchema(detail="Conductor no encontrado.", result=None)
        except Exception as e:
            print(f"Error updating driver by ID: {e}")
            return ResponseSchema(detail=f"An error occurred: {e}", result=None)

    @staticmethod
    async def delete_by_id(driver_id: int):
        result = await DriverRepository.delete(driver_id)
        if result:
            return ResponseSchema(detail="Conductor eliminado", result=result)
        else:
            return ResponseSchema(detail="Conductor no encontrado.", result=None)
