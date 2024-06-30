
from shared.response.schema import ResponseSchema
from unit_management.model.unit import CreateUnitModel
from unit_management.repository.unit_repository import UnitRepository


class UnitService:

    @staticmethod
    async def get_all():
        result = await UnitRepository.get_all()
        if result:
            return ResponseSchema(detail="Successfully get all data!", result=result)
        else:
            ResponseSchema(detail="Please get all data not found!", result=result)

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
            result = await UnitRepository.get_filtered(name)  # Potential error here
            if result:
                return ResponseSchema(detail="Successfully got driver by unit!", result=result)
            else:
                return ResponseSchema(detail="Unit name not found.", result=None)
        except Exception as e:  # Catch any exception
            print(f"Error retrieving unit by ID: {e}")  # Log the error
            return ResponseSchema(detail="An error occurred:", result=None)

    @staticmethod
    async def create(data: CreateUnitModel):
        result = await UnitRepository.create(data)
        if result:
            return ResponseSchema(detail="Successfully create unit!", result=result)
        else:
            return ResponseSchema(detail="Failed to create unit!", result=None)

    @staticmethod
    async def update(unit_id: int, data: CreateUnitModel):
        try:
            result = await UnitRepository.update(unit_id, data)
            if result:
                return ResponseSchema(detail="Successfully update unit!", result=result)
            else:
                return ResponseSchema(detail="Unit not found.", result=None)
        except Exception as e:
            print(f"Error updating unit by ID: {e}")
            return ResponseSchema(detail=f"An error occurred: {e} : no existe el driverId", result=None)

    @staticmethod
    async def delete_by_id(user_id: int):
        result = await UnitRepository.delete(user_id)
        if result:
            return ResponseSchema(detail="Successfully delete unit!", result=result)
        else:
            return ResponseSchema(detail="Unit not found.", result=None)