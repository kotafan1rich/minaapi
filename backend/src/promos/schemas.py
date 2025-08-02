from pydantic import BaseModel


class ResponsePromo(BaseModel):
    id: int
    description: str
