from fastapi import HTTPException

from shared.exception.validators import validate_existence
from shared.response.schema import ResponseSchema
from unit_management.model.unit import CreateUnitModel
from unit_management.repository.unit_repository import UnitRepository


class UnitService:

    @staticmethod
    async def get_all():
        result = await UnitRepository.get_all()
        if result:
            return ResponseSchema(detail="Data successfully obtained!", result=result)
        else:
            ResponseSchema(detail="Data successfully obtained!", result=result)

    @staticmethod
    async def get_by_id(driver_id: int):
        result = await UnitRepository.get_by_id(driver_id)
        if result:
            return ResponseSchema(detail="Successfully got unit by ID!", result=result)
        else:
            return ResponseSchema(detail="Please unit id not found.", result=None)

    # es un ejemplo para ver los errores en consola si es que hay
    @staticmethod
    async def get_filtered(name: str):
        try:
            result = await UnitRepository.get_by_car_plate(name)  # Potential error here
            if result:
                return ResponseSchema(detail="Successfully got driver by unit!", result=result)
            else:
                return ResponseSchema(detail="Unit name not found.", result=None)
        except Exception as e:  # Catch any exception
            print(f"Error retrieving unit by ID: {e}")  # Log the error
            return ResponseSchema(detail="An error occurred:", result=None)

    @staticmethod
    async def create(data: CreateUnitModel):
        existing_car_plate = await UnitRepository.get_by_car_plate(data.carPlate)
        if existing_car_plate:
            raise HTTPException(status_code=400, detail=f'La placa con el nombre {data.carPlate} ya existe')
        result = await UnitRepository.create(data)
        if result:
            return ResponseSchema(detail="Unidad creada exitosamente", result=result)
        else:
            raise HTTPException(status_code=500, detail="Error al crear unidad")  # Lanzar excepción en caso de error

    @staticmethod
    async def update(unit_id: int, data: CreateUnitModel):
        existing_unit = await UnitRepository.get_by_id(unit_id)
        validate_existence(existing_unit, unit_id, "Unidad")

        existing_unit_with_same_plate = await UnitRepository.get_by_car_plate(data.carPlate)

        # Si hay otra unidad con la misma placa y no es la unidad que estamos actualizando
        if existing_unit_with_same_plate and existing_unit_with_same_plate.id != unit_id:
            raise HTTPException(status_code=400, detail=f'Placa: {data.carPlate} ya está registrada')

        result = await UnitRepository.update(unit_id, data)
        if result:
            return ResponseSchema(detail="Unidad actualizada exitosamente", result=result)
        else:
            raise HTTPException(status_code=500, detail="Error al actualizar unidad!")

    @staticmethod
    async def delete_by_id(user_id: int):
        result = await UnitRepository.delete(user_id)
        if result:
            return ResponseSchema(detail="Unidad eliminada", result=result)
        else:
            return ResponseSchema(detail="Unit not found.", result=None)