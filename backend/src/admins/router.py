from fastapi import APIRouter, Depends
from src.admins.dao import AdminDAO
from src.admins.schemas import ResponseAdmin
from src.db.session import get_db

admin_router = APIRouter(prefix="/admins", tags=["Admins"])


@admin_router.post("/create_admin", response_model=ResponseAdmin)
async def create_admin(user_id: int, db_session=Depends(get_db)):
    admin_dao = AdminDAO(db_session=db_session)
    created_admin = await admin_dao.create_admin(user_id=user_id)
    if created_admin:
        return ResponseAdmin.model_validate(created_admin, from_attributes=True)


@admin_router.get("/get_admin", response_model=ResponseAdmin)
async def get_admin(id: int, db_session=Depends(get_db)):
    admin_dao = AdminDAO(db_session=db_session)
    admin = await admin_dao.get_admin(id=id)
    if admin:
        return ResponseAdmin.model_validate(admin, from_attributes=True)


@admin_router.get("/get_admin_by_user_id", response_model=ResponseAdmin)
async def get_admin_by_user_id(user_id: int, db_session=Depends(get_db)):
    admin_dao = AdminDAO(db_session=db_session)
    created_admin = await admin_dao.get_admin_by_user_id(user_id=user_id)
    if created_admin:
        return ResponseAdmin.model_validate(created_admin, from_attributes=True)
