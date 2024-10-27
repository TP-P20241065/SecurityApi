from pydantic import BaseModel


class CreateCameraModel(BaseModel):
    name: str
    location: str
    url: str
    unitId: int


class CameraModel(BaseModel):
    id: int
    name: str
    location: str
    unitId: int
    url: str
