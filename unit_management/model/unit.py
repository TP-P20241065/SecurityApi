from pydantic import BaseModel


class CreateUnitModel(BaseModel):
    car_plate: str
    driver_id: str


class UnitModel(BaseModel):
    id: int
    car_plate: str
    driver_id: str


