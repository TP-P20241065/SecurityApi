
from config.connection import prisma_connection
from unit_management.model.unit import CreateUnitModel


class UnitRepository:
    @staticmethod
    async def get_all():
        return await prisma_connection.prisma.unit.find_many()

    @staticmethod
    async def get_by_id(unit_id: int):
        return await prisma_connection.prisma.unit.find_first(where={"id": driver_id})

    @staticmethod
    async def get_filtered(_name: str):
        record = await prisma_connection.prisma.unit.find_many(where={"name": _name})
        # print(f"Record retrieved: {record}")  # Add console logging with f-string
        return record

    @staticmethod
    async def create(unit: CreateUnitModel):
        return await prisma_connection.prisma.driver.create({
            'car_plate': unit.car_plate,
            'driver_id': unit.driver_id
        })

    @staticmethod
    async def update(unit_id: int, unit: CreateUnitModel):
        return await prisma_connection.prisma.driver.update(where={"id": unit_id}, data={
            'car_plate': unit.car_plate,
            'driver_id': unit.driver_id
        })

    @staticmethod
    async def delete(unit_id: int):
        return await prisma_connection.prisma.driver.delete(where={"id": unit_id})
