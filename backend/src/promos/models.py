from sqlalchemy import Column, Integer, String
from src.db.models import BaseModel


class Promo(BaseModel):
    id = Column(Integer, primary_key=True)
    description = Column(String(4096), nullable=False)
