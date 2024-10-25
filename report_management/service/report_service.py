from fastapi import UploadFile
import base64
from config.connection import prisma_connection
from shared.response.schema import ResponseSchema, ResponseSchema2
from report_management.model.report import ReportCreate
from report_management.repository.report_repository import ReportRepository
from shared.message.message_service import send_alert, send_mms


class ReportService:

    @staticmethod
    async def get_all():
        try:
            result = await ReportRepository.get_all()
            if result:
                return ResponseSchema(detail="All data successfully received!", result=result)
            else:
                ResponseSchema(detail="Data not found!", result=result)
        except Exception as e:  # Catch any exception
            print(f"Error retrieving report by ID: {e}")  # Log the error
            return ResponseSchema(detail=f"An error occurred: {e}  (Está vacío)", result=None)

    @staticmethod
    async def get_by_id(report_id: int):
        result = await ReportRepository.get_by_id(report_id)
        if result:
            return ResponseSchema(detail="Report successfully received by id!", result=result)
        else:
            return ResponseSchema(detail="Report id not found.", result=None)

    # es un ejemplo para ver los errores en consola si es que hay
    @staticmethod
    async def get_filtered(name: str):
        try:
            result = await ReportRepository.get_filtered(name)  # Potential error here
            if result:
                return ResponseSchema(detail="Report successfully received by unit!", result=result)
            else:
                return ResponseSchema(detail="Report incident not found.", result=None)
        except Exception as e:  # Catch any exception
            print(f"Error retrieving report by ID: {e}")  # Log the error
            return ResponseSchema(detail="An error occurred:", result=None)

    @staticmethod
    async def create_report(address: str, incident: str, tracking_link: str, image: bytes, unit_id: int):
        encoded_image = base64.b64encode(image).decode('utf-8')
        return await prisma_connection.prisma.report.create(
            data={
                'address': address,
                'incident': incident,
                'trackingLink': tracking_link,
                'image': encoded_image,
                'unitId': unit_id,
            }
        )

    @staticmethod
    async def get_report(report_id: int):
        report = await prisma_connection.prisma.report.find_unique(
            where={'id': report_id}
        )
        return report

    @staticmethod
    async def get_report_image(report_id: int) -> str:
        report = await prisma_connection.prisma.report.find_unique(where={"id": report_id})
        if report and report.image:
            return f"data:image/jpeg;base64,{report.image}"
        else:
            return None

    @staticmethod
    async def update(report_id: int, data: ReportCreate):
        try:
            result = await ReportRepository.update(report_id, data)
            if result:
                return ResponseSchema(detail="Report successfully updated!", result=result)
            else:
                return ResponseSchema(detail="Report not found.", result=None)
        except Exception as e:
            print(f"Error updating unit by ID: {e}")
            return ResponseSchema(detail=f"An error occurred: {e} : No existe el unitId", result=None)

    @staticmethod
    async def delete_by_id(report_id: int):
        result = await ReportRepository.delete(report_id)
        if result:
            return ResponseSchema(detail="Report successfully deleted!", result=result)
        else:
            return ResponseSchema(detail="Report not found.", result=None)
