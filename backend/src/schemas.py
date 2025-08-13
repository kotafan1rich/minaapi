from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseResponseSchema(BaseModel):
    time_created: datetime
    time_updated: datetime

    model_config = ConfigDict(from_attributes=True)
