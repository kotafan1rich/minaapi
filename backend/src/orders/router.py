from fastapi import APIRouter, Depends, HTTPException, status
from src.db.session import get_db
from src.orders.dao import OrderDAO
from src.orders.schemas import ListOrders, RequestOrder, OrderSchema

order_router = APIRouter(prefix="/orders", tags=["Orders"])


@order_router.post("/create_order")
async def create_order(data: RequestOrder, db_session=Depends(get_db)) -> OrderSchema:
    order_dao = OrderDAO(db_session=db_session)
    created_order = await order_dao.create_order(**data.model_dump())
    if created_order:
        return OrderSchema.model_validate(created_order)


@order_router.get("/get_order_list")
async def get_order_list(
    offset: int = 0, limit: int = 10, db_session=Depends(get_db)
) -> ListOrders:
    order_dao = OrderDAO(db_session=db_session)
    orders_list = await order_dao.get_all_orders(offset=offset, limit=limit)
    if not orders_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Orders not found"
        )
    return ListOrders(
        results=[OrderSchema.model_validate(order) for order in orders_list]
    )


@order_router.get("/get_completed_orders_for_user")
async def get_completed_orders_for_user(
    user_id: int, db_session=Depends(get_db)
) -> ListOrders:
    order_dao = OrderDAO(db_session=db_session)
    result = await order_dao.get_completed_orders_for_user(user_id=user_id)
    if result:
        return ListOrders(result=result)
    else:
        raise HTTPException(status_code=404, detail="Orders not found")


@order_router.get("/get_active_orders")
async def get_active_orders(db_session=Depends(get_db)) -> ListOrders:
    order_dao = OrderDAO(db_session=db_session)
    result = await order_dao.get_active_orders()
    if result:
        return ListOrders(
            results=[OrderSchema.model_validate(order) for order in result]
        )
    else:
        raise HTTPException(status_code=404, detail="Orders not found")


@order_router.get("/get_completed_orders")
async def get_completed_orders(db_session=Depends(get_db)) -> ListOrders:
    order_dao = OrderDAO(db_session=db_session)
    result = await order_dao.get_completed_orders()
    if result:
        return ListOrders(
            result=[OrderSchema.model_validate(order) for order in result]
        )
    else:
        raise HTTPException(status_code=404, detail="Orders not found")


@order_router.patch("/update_order")
async def update_order(
    id: int, data: RequestOrder, db_session=Depends(get_db)
) -> OrderSchema:
    order_dao = OrderDAO(db_session=db_session)
    updated_order = await order_dao.update_order(id=id, **data.model_dump())
    if updated_order:
        return OrderSchema.model_validate(updated_order)


@order_router.delete("/delete_order")
async def delete_order(id: int, db_session=Depends(get_db)) -> OrderSchema:
    order_dao = OrderDAO(db_session=db_session)
    updated_order = await order_dao.delete_order(id=id)
    if updated_order:
        return OrderSchema.model_validate(updated_order)
