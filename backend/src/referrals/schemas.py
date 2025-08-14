from pydantic import BaseModel
from src.schemas import BaseResponseSchema


class ReferralSchema(BaseResponseSchema):
    id_from: int
    id_to: int


class ListReferrals(BaseModel):
    results: list[int]
