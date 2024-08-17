from typing import Any, List, Optional
from pydantic import BaseModel


class Excursion(BaseModel):
    excur_id: int
    name: str
    description: str
    price: float
    photo: str


class Excursions(BaseModel):
    excursions: List[Excursion]

class DeleteExcursion(BaseModel):
    excur_id: int


class EditExcursion(BaseModel):
    excur_id: int
    name: str | None = None
    description: str | None = None
    price: float | None = None

class SuccessfulPayment(BaseModel):
    username: str
    excur_id: int