
from enum import Enum as PyEnum
from sqlalchemy import BIGINT, Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.db.models import BaseModel


class OrderStatus(PyEnum):
    CREATED = "Создан"
    PAID = "Заказ оплачен"
    BOUGHT_OUT = "Выкуплен"
    AGENT = "Передан Агенту"
    CUSTOMS = "Таможня"
    MOSCOW_WAREHOUSE = "На складе в Москве"
    TO_PETERSBURG = "Едет в Питер"
    TO_CUSTOMER_CITY = "Едет в город к покупателю"
    COMPLETED = "Завершен"
    CANCELED = "Отменён"


class OrderTypeItem(PyEnum):
    SHOES = "Обувь"
    CLOTH = "Одежда"


class Order(BaseModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(BIGINT, ForeignKey("users.id"), nullable=False)
    status: OrderStatus = Column(
        Enum(OrderStatus), default=OrderStatus.CREATED, nullable=False
    )
    article = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    price_rub = Column(Float, nullable=False, default=0.0)
    price_cny = Column(Integer, nullable=False, default=0)
    size = Column(String(100), nullable=False)
    type_item: OrderStatus = Column(
        Enum(OrderTypeItem), default=OrderTypeItem.SHOES, nullable=False
    )

    user = relationship("User", back_populates="orders")