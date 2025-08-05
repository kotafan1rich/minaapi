from src.schemas import BaseResponseSchema


class ResponsePromo(BaseResponseSchema):
    id: int
    description: str
