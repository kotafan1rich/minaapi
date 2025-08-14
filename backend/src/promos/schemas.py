from typing import List

from pydantic import BaseModel
from src.schemas import BaseResponseSchema


class PromoSchema(BaseResponseSchema):
    id: int
    description: str


class ListPromos(BaseModel):
    results: List[PromoSchema]
