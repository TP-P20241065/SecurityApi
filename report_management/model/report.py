from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional,BinaryIO


class ReportCreate(BaseModel):
    address: Optional[str]
    incident: Optional[str]
    trackingLink: Optional[str]
    unitId: Optional[int]

    class Config:
        from_attributes = True


class ReportModel(BaseModel):
    id: int
    address: Optional[str]
    incident: Optional[str]
    trackingLink: Optional[str]
    image: Optional[bytes]
    unitId: Optional[int]