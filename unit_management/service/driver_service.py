from typing import Dict

from fastapi import HTTPException

from shared.exception.validators import validate_existence, validate_uniqueness_single_by_id, validate_uniqueness_single
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
        existing_item_duplicate = await DriverRepository.get_driver_by_dni(data.dni)
        validate_uniqueness_single(existing_item_duplicate, 'dni', data.dni)

        result = await DriverRepository.create(data)
        if result:
            return ResponseSchema(detail="Conductor creado!", result=result)
        else:
            raise HTTPException(status_code=500, detail="Error al crear conductor")

    @staticmethod
    async def update(driver_id: int, data: CreateDriverModel):
        # valida si existe el objeto y da las respuesta correspondiente
        existing_item = await DriverRepository.get_by_id(driver_id)
        validate_existence(existing_item, driver_id, "Conductor")
        # valida si ya existen objetos con atributos duplicados
        existing_item_duplicate = await DriverRepository.get_driver_by_dni(data.dni)
        validate_uniqueness_single_by_id(existing_item_duplicate, driver_id, 'dni', data.dni)
        result = await DriverRepository.update(driver_id, data)
        if result:
            return ResponseSchema(detail="Conductor actualizado exitosamente", result=result)
        else:
            raise HTTPException(status_code=500, detail="Error al actualizar conductor!")

    @staticmethod
    async def delete_by_id(driver_id: int):
        result = await DriverRepository.delete(driver_id)
        if result:
            return ResponseSchema(detail="Conductor eliminado", result=result)
        else:
            return ResponseSchema(detail="Conductor no encontrado.", result=None)
