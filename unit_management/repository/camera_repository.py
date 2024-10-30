from config.connection import prisma_connection
from unit_management.model.camera import CreateCameraModel


class CameraRepository:
    @staticmethod
    async def get_all():
        return await prisma_connection.prisma.camera.find_many()

    @staticmethod
    async def get_by_id(camera_id: int):
        return await prisma_connection.prisma.camera.find_first(where={"id": camera_id})

    @staticmethod
    async def get_filtered(_name: str):
        record = await prisma_connection.prisma.camera.find_many(where={"name": _name})
        # print(f"Record retrieved: {record}")  # Add console logging with f-string
        return record

    @staticmethod
    async def create(camera: CreateCameraModel):
        return await prisma_connection.prisma.camera.create({
            'name': camera.name,
            'location': camera.location,
            'url': camera.url,
            'unitId': camera.unitId,
        })

    @staticmethod
    async def update(camera_id: int, camera: CreateCameraModel):
        return await prisma_connection.prisma.camera.update(where={"id": camera_id}, data={
            'name': camera.name,
            'location': camera.location,
            'url': camera.url,
            'unitId': camera.unitId,
        })

    @staticmethod
    async def delete(unit_id: int):
        return await prisma_connection.prisma.camera.delete(where={"id": unit_id})

    @staticmethod
    async def get_cameras_by_name_url(name: str, url: str):
        return await prisma_connection.prisma.camera.find_many(
            where={
                "OR": [
                    {"name": name},
                    {"url": url,
                     "NOT": {
                         "url": "0"
                     }
                     }
                ]
            }
        )
