from fastapi import APIRouter, Depends, HTTPException, status
from src.auth.utils import get_hash
from src.db.session import get_db
from src.users.dao import UserDAO
from src.users.schemas import ListUsers, RequestUpdateUser, RequestUser, ResponseUser
from src.users.utils import _create_user

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/create_user")
async def create_user(data: RequestUser, db_session=Depends(get_db)) -> ResponseUser:
    created_user = await _create_user(data=data, db_session=db_session)
    if created_user:
        return ResponseUser.model_validate(created_user)


@user_router.delete("/delete_user")
async def delete_user(id: int, db_session=Depends(get_db)) -> ResponseUser:
    user_dao = UserDAO(db_session=db_session)
    deleted_user = await user_dao.delete_user(id=id)
    if deleted_user:
        return ResponseUser.model_validate(deleted_user)


@user_router.get("/get_user")
async def get_user(id: int, db_session=Depends(get_db)) -> ResponseUser:
    user_dao = UserDAO(db_session=db_session)
    user = await user_dao.get_user_by_id(id=id)
    if user:
        return ResponseUser.model_validate(user)
    else:
        raise HTTPException(status_code=404, detail="User not found")


@user_router.get("/get_users_list")
async def get_userls_list(
    offset: int = 0, limit: int = 10, db_session=Depends(get_db)
) -> ListUsers:
    user_dao = UserDAO(db_session=db_session)
    users_list = await user_dao.get_all_users(offset=offset, limit=limit)
    if not users_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Users not found"
        )
    return ListUsers(results=[ResponseUser.model_validate(user) for user in users_list])


@user_router.patch("/update_user")
async def update_user(
    id: int, data: RequestUpdateUser, db_session=Depends(get_db)
) -> ResponseUser:
    user_dao = UserDAO(db_session=db_session)
    data_dict = data.model_dump()
    password = data.password
    if password:
        hashed_password = get_hash(password)
        data_dict["hashed_password"] = hashed_password
    data_dict.pop("password")
    data_dict = {key: val for key, val in data_dict.items() if val}
    created_user = await user_dao.update_user(id=id, **data_dict)
    if created_user:
        return ResponseUser.model_validate(created_user)
