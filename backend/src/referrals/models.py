from sqlalchemy import BIGINT, Column, ForeignKey, Index, Integer, UniqueConstraint
from src.db.models import BaseModel
from sqlalchemy.orm import relationship


class Referral(BaseModel):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True)
    id_from = Column(
        BIGINT, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    id_to = Column(
        BIGINT,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    referrer = relationship(
        "User",
        foreign_keys=[id_from],
        back_populates="referrals_from",
    )
    referree = relationship(
        "User",
        foreign_keys=[id_to],
        back_populates="referrals_to",
    )

    __table_args__ = (
        UniqueConstraint("id_from", "id_to", name="unique_referral"),
        Index("ix_user_id", "id_from", "id_to"),
    )
