from typing import Dict

from unit_management.model.driver import CreateDriverModel
from config.connection import prisma_connection


# solo mantiene comuniacion con la base de datos
class DriverRepository:

    @staticmethod
    async def get_all():
        return await prisma_connection.prisma.driver.find_many()

    @staticmethod
    async def get_by_id(driver_id: int):
        return await prisma_connection.prisma.driver.find_first(where={"id": driver_id})

    @staticmethod
    async def get_filtered(name: str):
        record = await prisma_connection.prisma.driver.find_many(where={"name": name})
        # print(f"Record retrieved: {record}")  # Add console logging with f-string
        return record

    @staticmethod
    async def create(driver: CreateDriverModel):
        return await prisma_connection.prisma.driver.create({
            'name': driver.name,
            'lastName': driver.lastName,
            'dni': driver.dni,
        })

    @staticmethod
    async def update(driver_id: int, driver: CreateDriverModel):
        return await prisma_connection.prisma.driver.update(where={"id": driver_id}, data={
            'name': driver.name,
            'lastName': driver.lastName,
            'dni': driver.dni
        })

    @staticmethod
    async def delete(driver_id: int):
        return await prisma_connection.prisma.driver.delete(where={"id": driver_id})
