from unit_management.model.driver import CreateDriverModel
from unit_management.repository.driver_repository import DriverRepository


class DriverService:

    @staticmethod
    async def get_all():
        return await DriverRepository.get_all()

    @staticmethod
    async def get_by_id(driver_id: int):
        return await DriverRepository.get_by_id(driver_id)

    @staticmethod
    async def get_by_name(name: str):
        return await DriverRepository.get_by_name(name)

    @staticmethod
    async def create(data: CreateDriverModel):
        return await DriverRepository.create(data)

    @staticmethod
    async def update(driver_id: int, data: CreateDriverModel):
        return await DriverRepository.update(driver_id, data)

    @staticmethod
    async def delete_by_id(driver_id: int):
        return await DriverRepository.delete(driver_id)
