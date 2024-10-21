from pydantic import BaseModel


class CreateCameraModel(BaseModel):
    name: str
    location: str
    unitId: int
    url: str



class CameraModel(BaseModel):
    id: int
    name: str
    location: str
    unitId: int
    url: str
