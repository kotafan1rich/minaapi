from fastapi import APIRouter, Depends

from src.db.session import get_db
from src.users.dao import UserDAO
from src.users.schemas import ResponseUser, RequestUser
from src.utils import get_hash


user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/create_user", response_model=ResponseUser)
async def create_user(data: RequestUser, db_session=Depends(get_db)):
    user_dao = UserDAO(db_session=db_session)
    data_dict = data.model_dump()
    hashed_password = get_hash(data.password)
    data_dict["hashed_password"] = hashed_password
    data_dict.pop("password")
    created_user = await user_dao.create_user(**data_dict)
    if created_user:
        return ResponseUser.model_validate(created_user, from_attributes=True)
