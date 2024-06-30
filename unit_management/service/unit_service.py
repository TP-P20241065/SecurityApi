
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
            return ResponseSchema(detail="Successfully got driver by ID!", result=result)
        else:
            return ResponseSchema(detail="Please driver id not found.", result=None)

    # es un ejemplo para ver los errores en consola si es que hay
    @staticmethod
    async def get_filtered(name: str):
        try:
            result = await UnitRepository.get_filtered(name)  # Potential error here
            if result:
                return ResponseSchema(detail="Successfully got driver by name!", result=result)
            else:
                return ResponseSchema(detail="Driver name not found.", result=None)
        except Exception as e:  # Catch any exception
            print(f"Error retrieving driver by ID: {e}")  # Log the error
            return ResponseSchema(detail="An error occurred:", result=None)

    @staticmethod
    async def create(data: CreateUnitModel):
        result = await UnitRepository.create(data)
        if result:
            return ResponseSchema(detail="Successfully create driver!", result=result)
        else:
            return ResponseSchema(detail="Failed to create driver!", result=None)

    @staticmethod
    async def update(user_id: int, data: CreateUnitModel):
        try:
            result = await UnitRepository.update(user_id, data)
            if result:
                return ResponseSchema(detail="Successfully update driver!", result=result)
            else:
                return ResponseSchema(detail="Driver not found.", result=None)
        except Exception as e:
            print(f"Error updating driver by ID: {e}")
            return ResponseSchema(detail=f"An error occurred: {e}", result=None)

    @staticmethod
    async def delete_by_id(user_id: int):
        result = await UnitRepository.delete(user_id)
        if result:
            return ResponseSchema(detail="Successfully delete driver!", result=result)
        else:
            return ResponseSchema(detail="Driver not found.", result=None)