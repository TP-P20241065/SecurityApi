from pydantic import BaseModel


class CreateUnitModel(BaseModel):
    carPlate: str
    driverId: int


class UnitModel(BaseModel):
    id: int
    carPlate: str
    driverId: int
