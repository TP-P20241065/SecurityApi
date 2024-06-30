from pydantic import BaseModel


class CreateCameraModel(BaseModel):
    name: str
    last_name: str
    dni: int
    image: str


class CameraModel(BaseModel):
    id: int
    name: str
    last_name: str
    dni: int
    image: str