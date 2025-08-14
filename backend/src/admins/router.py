from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from src.admins.dao import AdminDAO
from src.admins.schemas import AdminSchema, ResponseAdminList
from src.db.session import get_db

admin_router = APIRouter(prefix="/admins", tags=["Admins"])


@admin_router.post("/create_admin")
async def create_admin(user_id: int, db_session=Depends(get_db)) -> AdminSchema:
    admin_dao = AdminDAO(db_session=db_session)
    created_admin = await admin_dao.create_admin(user_id=user_id)
    if created_admin:
        return AdminSchema.model_validate(created_admin)


@admin_router.delete("/delete_admin")
async def delete_admin(id: int, db_session=Depends(get_db)) -> AdminSchema:
    admin_dao = AdminDAO(db_session=db_session)
    deleted_admin = await admin_dao.delete_admin(id=id)
    if not deleted_admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found"
        )
    return AdminSchema.model_validate(deleted_admin)


@admin_router.get("/get_admin")
async def get_admin(id: int, db_session=Depends(get_db)) -> AdminSchema:
    admin_dao = AdminDAO(db_session=db_session)
    admin = await admin_dao.get_admin(id=id)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found"
        )
    return AdminSchema.model_validate(admin)


@admin_router.get("/get_admins_list")
async def get_admins_list(
    offset: int = 0, limit: int = 10, db_session=Depends(get_db)
) -> ResponseAdminList:
    admin_dao = AdminDAO(db_session=db_session)
    admins_list = await admin_dao.get_all_admins(offset=offset, limit=limit)
    if not admins_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Admins not found"
        )
    return ResponseAdminList(
        results=[AdminSchema.model_validate(admin) for admin in admins_list]
    )


@admin_router.get("/get_admin_by_user_id")
async def get_admin_by_user_id(
    user_id: int, db_session=Depends(get_db)
) -> AdminSchema:
    admin_dao = AdminDAO(db_session=db_session)
    created_admin = await admin_dao.get_admin_by_user_id(user_id=user_id)
    if created_admin:
        return AdminSchema.model_validate(created_admin)
