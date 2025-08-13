from typing import List
from pydantic import BaseModel
from src.schemas import BaseResponseSchema


class ResponseSetting(BaseResponseSchema):
    id: int
    key: str
    value: float


class ResponseSettingsList(BaseModel):
    results: List[ResponseSetting]
