from sqlalchemy import select
from src.admins.models import Admin
from src.db.dao import BaseDAO


class AdminDAO(BaseDAO):
    async def create_admin(self, user_id: int):
        async with self.db_session.begin():
            new_admin = Admin(user_id=user_id)
            self.db_session.add(new_admin)
            await self.db_session.commit()
            return new_admin
    
    async def get_admin(self, id: int) -> Admin | None:
        async with self.db_session.begin():
            query = select(Admin).where(Admin.id == id)
            result = await self.db_session.execute(query)
            return result.scalar_one_or_none()
    
    async def get_admin_by_user_id(self, user_id: int) -> Admin | None:
        async with self.db_session.begin():
            query = select(Admin).where(Admin.id == user_id)
            result = await self.db_session.execute(query)
            return result.scalar_one_or_none()
