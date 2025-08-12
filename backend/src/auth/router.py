from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from src.auth.schemas import Token
from src.auth.utils import create_access_token, verify_password
from src.db.session import get_db
from src.users.dao import UserDAO
from src.users.schemas import RequestUser, ResponseUser
from src.users.utils import _create_user
from src.config import settings


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register", response_model=ResponseUser)
async def register(data: RequestUser, db_session=Depends(get_db)):
    created_user = await _create_user(data=data, db_session=db_session)
    if created_user:
        return ResponseUser.model_validate(created_user, from_attributes=True)


@auth_router.post("/login", response_model=Token)
async def login(email: str, password: str, db_session=Depends(get_db)):
    user_dao = UserDAO(db_session=db_session)
    user = await user_dao.get_user_by_email(email=email)
    if not user or not verify_password(
        password=password, hashed_password=user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Wrong email or password")
    created_jwt = create_access_token(
        user.id, expires_delta=timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return Token(access_token=created_jwt, token_type="bearer")
