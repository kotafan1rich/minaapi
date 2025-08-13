from typing import List

from pydantic import BaseModel
from src.schemas import BaseResponseSchema


class ResponsePromo(BaseResponseSchema):
    id: int
    description: str


class ListPromos(BaseModel):
    results: List[ResponsePromo]
