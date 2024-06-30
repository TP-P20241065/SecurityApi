from unit_management.model.driver import CreateDriverModel
from config.connection import prisma_connection


class DriverRepository:

    @staticmethod
    async def get_all():
        return await prisma_connection.prisma.driver.find_many()

    @staticmethod
    async def get_by_id(driver_id: int):
        return await prisma_connection.prisma.driver.find_first(where={"id": driver_id})

    @staticmethod
    async def get_by_name(name: str):
        return await prisma_connection.prisma.driver.find_first(where={"name": name})

    @staticmethod
    async def create(driver: CreateDriverModel):
        return await prisma_connection.prisma.driver.create({
            'name': driver.name,
            'lastName': driver.last_name,
            'dni': driver.dni,
            'image': driver.image
        })

    @staticmethod
    async def update(driver_id: int, driver: CreateDriverModel):
        return await prisma_connection.prisma.driver.update(where={"id": driver_id}, data={
            'name': driver.name,
            'lastName': driver.last_name,
            'dni': driver.first_name,
            'image': driver.first_name
        })

    @staticmethod
    async def delete(driver_id: int):
        return await prisma_connection.prisma.driver.delete(driver_id)
