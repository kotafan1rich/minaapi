from pydantic import BaseModel, EmailStr


class BaseUserSchema(BaseModel):
    tg_id: int = None
    tg_username: str = None
    email: EmailStr = None


class RequestUser(BaseUserSchema):
    password: str


class ResponseUser(BaseUserSchema):
    id: int
    hashed_password: str
