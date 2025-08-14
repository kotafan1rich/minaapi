from typing import List
from pydantic import BaseModel
from src.schemas import BaseResponseSchema


class SettingSchema(BaseResponseSchema):
    id: int
    key: str
    value: float


class ResponseSettingsList(BaseModel):
    results: List[SettingSchema]
