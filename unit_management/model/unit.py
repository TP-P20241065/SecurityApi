from pydantic import BaseModel


class CreateUnitModel(BaseModel):
    name: str
    last_name: str
    dni: int
    image: str


class UnitModel(BaseModel):
    id: int
    name: str
    last_name: str
    dni: int
    image: str

