from typing import List
from pydantic import BaseModel, EmailStr

from src.schemas import BaseResponseSchema


class BaseUserSchema(BaseModel):
    tg_id: int | None = None
    tg_username: str | None = None
    email: EmailStr | None = None


class RequestUser(BaseUserSchema):
    password: str


class RequestUpdateUser(BaseUserSchema):
    password: str | None = None


class ResponseUser(BaseResponseSchema, BaseUserSchema):
    id: int
    hashed_password: str


class ListUsers(BaseModel):
    results: List[ResponseUser]
