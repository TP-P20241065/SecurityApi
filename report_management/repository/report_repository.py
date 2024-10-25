from config.connection import prisma_connection
from report_management.model.report import ReportCreate, ReportModel


class ReportRepository:
    @staticmethod
    async def get_all():
        return await prisma_connection.prisma.report.find_many()

    @staticmethod
    async def get_by_id(report_id: int):
        return await prisma_connection.prisma.report.find_first(where={"id": report_id})

    @staticmethod
    async def get_filtered(_name: str):
        record = await prisma_connection.prisma.report.find_many(where={"incident": _name})
        # print(f"Record retrieved: {record}")  # Add console logging with f-string
        return record

    @staticmethod
    async def create(data: dict):
        return await prisma_connection.prisma.report.create(data=data)

    @staticmethod
    async def update(report_id: int, report: ReportCreate):

        return await prisma_connection.prisma.report.update(where={"id": report_id}, data={
            'address': report.address,
            'incident': report.incident,
            'trackingLink': report.trackingLink,
            'unitId': report.unitId
        })


    @staticmethod
    async def delete(report_id: int):
        return await prisma_connection.prisma.report.delete(where={"id": report_id})
