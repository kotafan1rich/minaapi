from sqlalchemy import BIGINT, Column, Float, String

from src.db.models import BaseModel


class AppSetting(BaseModel):
    id = Column(BIGINT, primary_key=True)
    key = Column(String(50), unique=True, nullable=False)
    value = Column(Float, nullable=False)
