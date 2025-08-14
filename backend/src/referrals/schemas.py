from pydantic import BaseModel
from src.schemas import BaseResponseSchema


class ReferralSchema(BaseResponseSchema):
    id: int
    id_from: int
    id_to: int


class ListReferrals(BaseModel):
    results: list[ReferralSchema]
