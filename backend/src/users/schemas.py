from pydantic import BaseModel, EmailStr

from src.schemas import BaseResponseSchema


class BaseUserSchema(BaseModel):
    tg_id: int | None = None
    tg_username: str | None = None
    email: EmailStr | None = None


class RequestUser(BaseUserSchema):
    password: str


class ResponseUser(BaseResponseSchema, BaseUserSchema):
    id: int
    hashed_password: str
