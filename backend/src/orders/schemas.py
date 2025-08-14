from pydantic import BaseModel
from src.orders.models import OrderStatus, OrderTypeItem
from src.schemas import BaseResponseSchema


class OrderBase(BaseModel):
    user_id: int
    status: OrderStatus
    article: str
    address: str
    price_rub: float
    price_cny: int
    size: str
    type_item: OrderTypeItem


class OrderSchema(BaseResponseSchema, OrderBase):
    id: int


class RequestOrder(OrderBase): ...


class ListOrders(BaseModel):
    results: list[OrderSchema]
