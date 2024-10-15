from pydantic import BaseModel


class CreateReportModel(BaseModel):
    address: str
    incident: str
    trackingLink: str
    image: bytes
    unitId: int


class ReportModel(BaseModel):
    id: int
    address: str
    incident: str
    trackingLink: str
    image: bytes
    unitId: int
