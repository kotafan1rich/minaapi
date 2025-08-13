from typing import List

from pydantic import EmailStr
from sqlalchemy import delete, exists, select, update
from src.db.dao import BaseDAO
from src.users.models import User


class UserDAO(BaseDAO):
    async def create_user(
        self,
        tg_id: int = None,
        tg_username: str = None,
        email: EmailStr = None,
        hashed_password: str = None,
    ) -> User | None:
        async with self.db_session.begin():
            new_user = User(
                tg_id=tg_id,
                tg_username=tg_username,
                email=email,
                hashed_password=hashed_password,
            )
            self.db_session.add(new_user)
            await self.db_session.commit()
            return new_user

    async def update_user(self, id: int, **kwargs) -> User | None:
        async with self.db_session.begin():
            query = update(User).where(User.id == id).values(kwargs).returning(User)
            res = await self.db_session.execute(query)
            await self.db_session.commit()
            return res.scalar_one_or_none()

    async def user_exists(self, id: int) -> bool:
        async with self.db_session.begin():
            query = select(exists().where(User.id == id))
            res = await self.db_session.execute(query)
            return res.scalar()

    async def get_user_by_id(self, id: int) -> User | None:
        async with self.db_session.begin():
            query = select(User).where(User.id == id)
            res = await self.db_session.execute(query)
            return res.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        async with self.db_session.begin():
            query = select(User).where(User.email == email)
            res = await self.db_session.execute(query)
            return res.scalar_one_or_none()

    async def get_all_users(self, offset: int, limit: int) -> List[User | None]:
        async with self.db_session.begin():
            query = select(User).offset(offset).limit(limit)
            result = await self.db_session.execute(query)
            return result.scalars().all()

    async def delete_user(self, id: int) -> User | None:
        async with self.db_session.begin():
            query = delete(User).where(User.id == id).returning(User)
            deleted_user = await self.db_session.execute(query)
            await self.db_session.commit()
            return deleted_user.scalar_one_or_none()
