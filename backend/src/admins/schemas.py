from typing import List
from pydantic import BaseModel
from src.schemas import BaseResponseSchema


class AdminSchema(BaseResponseSchema):
    id: int
    user_id: int


class ResponseAdminList(BaseModel):
    results: List[AdminSchema]
