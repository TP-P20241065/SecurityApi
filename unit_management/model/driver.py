from pydantic import BaseModel


class CreateDriverModel(BaseModel):
    name: str
    lastName: str
    dni: int
    image: bytes


class DriverModel(BaseModel):
    id: int
    name: str
    lastName: str
    dni: int
    image: bytes


