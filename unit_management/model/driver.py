from pydantic import BaseModel


class CreateDriverModel(BaseModel):
    name: str
    lastName: str
    dni: int


class DriverModel(BaseModel):
    id: int
    name: str
    lastName: str
    dni: int


