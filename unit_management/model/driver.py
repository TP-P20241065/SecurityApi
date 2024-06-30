from pydantic import BaseModel


class CreateDriverModel(BaseModel):
    name: str
    last_name: str
    dni: int
    image: str


class DriverModel(BaseModel):
    id: int
    name: str
    last_name: str
    dni: int
    image: str


