from shared.response.schema import ResponseSchema
from report_management.model.report import CreateReportModel
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
    async def create(data: CreateReportModel):
        result = await ReportRepository.create(data)
        message = send_alert(data.address, data.incident, data.trackingLink, data.image, data.unitId)
        await send_mms(message)
        if result:
            return ResponseSchema(detail="Report successfully created!", result=result)
        else:
            return ResponseSchema(detail="Failed to create report!", result=None)

    @staticmethod
    async def update(report_id: int, data: CreateReportModel):
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
