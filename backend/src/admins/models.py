from sqlalchemy import BIGINT, Column, ForeignKey
from sqlalchemy.orm import relationship
from src.db.models import BaseModel


class Admin(BaseModel):
    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="admin")
