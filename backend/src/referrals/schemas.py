from pydantic import BaseModel
from src.schemas import BaseResponseSchema


class ResponseReferral(BaseResponseSchema):
    id_from: int
    id_to: int


class ListReferrals(BaseModel):
    result: list[int]
