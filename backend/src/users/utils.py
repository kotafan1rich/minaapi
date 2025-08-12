from src.auth.utils import get_hash
from src.users.dao import UserDAO
from src.users.models import User
from src.users.schemas import RequestUser


async def _create_user(data: RequestUser, db_session) -> User | None:
    user_dao = UserDAO(db_session=db_session)
    data_dict = data.model_dump()
    hashed_password = get_hash(data.password)
    data_dict["hashed_password"] = hashed_password
    data_dict.pop("password")
    created_user = await user_dao.create_user(**data_dict)
    return created_user