from fastapi import APIRouter, Depends, HTTPException

from src.db.session import get_db
from src.users.dao import UserDAO
from src.users.schemas import RequestUpdateUser, ResponseUser, RequestUser
from src.auth.utils import get_hash
from src.users.utils import _create_user


user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/create_user", response_model=ResponseUser)
async def create_user(data: RequestUser, db_session=Depends(get_db)):
    created_user = await _create_user(data=data, db_session=db_session)
    if created_user:
        return ResponseUser.model_validate(created_user, from_attributes=True)


@user_router.get("/get_user", response_model=ResponseUser)
async def get_user(id: int, db_session=Depends(get_db)):
    user_dao = UserDAO(db_session=db_session)
    user = await user_dao.get_user_by_id(id=id)
    if user:
        return ResponseUser.model_validate(user, from_attributes=True)
    else:
        raise HTTPException(status_code=404, detail="User not found")


@user_router.patch("/update_user", response_model=ResponseUser)
async def update_user(id: int, data: RequestUpdateUser, db_session=Depends(get_db)):
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
        return ResponseUser.model_validate(created_user, from_attributes=True)
