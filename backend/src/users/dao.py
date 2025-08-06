from pydantic import EmailStr
from sqlalchemy import exists, select, update

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
            query = (
                update(User)
                .where(User.id == id)
                .values(kwargs)
                .returning(User)
            )
            res = await self.db_session.execute(query)
            await self.db_session.commit()
            return res.scalar_one_or_none()

    async def user_exists(self, id: int) -> bool:
        async with self.db_session.begin():
            query = select(exists().where(User.id == id))
            res = await self.db_session.execute(query)
            return res.scalar()

    async def get_user(self, id: int) -> User | None:
        async with self.db_session.begin():
            query = select(User).where(User.id == id)
            res = await self.db_session.execute(query)
            return res.scalar()
