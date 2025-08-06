from src.schemas import BaseResponseSchema


class ResponseAdmin(BaseResponseSchema):
    id: int
    user_id: int
