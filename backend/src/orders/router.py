from fastapi import APIRouter, Depends, HTTPException

from src.db.session import get_db
from src.orders.dao import OrderDAO
from src.orders.schemas import ListOrders, RequestOrder, ResponseOrder


order_router = APIRouter(prefix="/orders", tags=["Orders"])


@order_router.post("/create_order", response_model=ResponseOrder)
async def create_order(data: RequestOrder, db_session=Depends(get_db)):
    order_dao = OrderDAO(db_session=db_session)
    created_order = await order_dao.create_order(**data.model_dump())
    if created_order:
        return ResponseOrder.model_validate(created_order, from_attributes=True)


@order_router.get("/get_completed_orders_for_user", response_model=ListOrders)
async def get_completed_orders_for_user(user_id: int, db_session=Depends(get_db)):
    order_dao = OrderDAO(db_session=db_session)
    result = await order_dao.get_completed_orders_for_user(user_id=user_id)
    if result:
        return ListOrders(result=result)
    else:
        raise HTTPException(status_code=404, detail="Orders not found")


@order_router.get("/get_active_orders", response_model=ListOrders)
async def get_active_orders(db_session=Depends(get_db)):
    order_dao = OrderDAO(db_session=db_session)
    result = await order_dao.get_active_orders()
    if result:
        return ListOrders(
            result=[
                ResponseOrder.model_validate(order, from_attributes=True)
                for order in result
            ]
        )
    else:
        raise HTTPException(status_code=404, detail="Orders not found")


@order_router.get("/get_completed_orders", response_model=ListOrders)
async def get_completed_orders(db_session=Depends(get_db)):
    order_dao = OrderDAO(db_session=db_session)
    result = await order_dao.get_completed_orders()
    if result:
        return ListOrders(
            result=[
                ResponseOrder.model_validate(order, from_attributes=True)
                for order in result
            ]
        )
    else:
        raise HTTPException(status_code=404, detail="Orders not found")


@order_router.patch("/update_order", response_model=ResponseOrder)
async def update_order(id: int, data: RequestOrder, db_session=Depends(get_db)):
    order_dao = OrderDAO(db_session=db_session)
    updated_order = await order_dao.update_order(id=id, **data.model_dump())
    if updated_order:
        return ResponseOrder.model_validate(updated_order, from_attributes=True)


@order_router.delete("/delete_order", response_model=ResponseOrder)
async def delete_order(id: int, db_session=Depends(get_db)):
    order_dao = OrderDAO(db_session=db_session)
    updated_order = await order_dao.delete_order(id=id)
    if updated_order:
        return ResponseOrder.model_validate(updated_order, from_attributes=True)

