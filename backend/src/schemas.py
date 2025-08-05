from datetime import datetime

from pydantic import BaseModel


class BaseResponseSchema(BaseModel):
    time_created: datetime
    time_updated: datetime
