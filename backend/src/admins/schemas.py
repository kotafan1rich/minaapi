from typing import List
from pydantic import BaseModel
from src.schemas import BaseResponseSchema


class ResponseAdmin(BaseResponseSchema):
    id: int
    user_id: int


class ResponseAdminList(BaseModel):
    results: List[ResponseAdmin]
