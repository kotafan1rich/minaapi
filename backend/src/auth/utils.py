from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from src.config import settings
from src.users.dao import UserDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="JWT-Token")


def get_hash(string: str) -> str:
    return pwd_context.hash(string)


def verify_password(password: str, hashed_password) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(user_id: int, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = {"sub": user_id}
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_jwt(token: str):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


async def get_current_user(db_session, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    user_dao = UserDAO(db_session=db_session)
    user = await user_dao.get_user_by_id(id=user_id)
    if user is None:
        raise credentials_exception
    return user
