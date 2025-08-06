from src.schemas import BaseResponseSchema


class ResponseSetting(BaseResponseSchema):
    id: int
    key: str
    value: float
