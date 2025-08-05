from sqlalchemy import BIGINT, Column, String
from sqlalchemy.orm import relationship
from src.db.models import BaseModel


class User(BaseModel):
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    tg_id = Column(BIGINT, unique=True, nullable=True)
    tg_username = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)

    referrals_from = relationship(
        "Referral",
        foreign_keys="Referral.id_from",
        back_populates="referrer",
    )
    referrals_to = relationship(
        "Referral",
        foreign_keys="Referral.id_to",
        back_populates="referree",
    )
    # orders = relationship("Order", back_populates="user")