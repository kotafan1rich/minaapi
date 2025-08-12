from sqlalchemy import delete, exists, select, update
from src.app_settings.models import AppSetting
from src.cache.redis import build_key, cached
from src.db.dao import BaseDAO


class AppSettingDAO(BaseDAO):
    async def param_exists(self, key: str) -> bool:
        async with self.db_session.begin():
            query = select(exists().where(AppSetting.key == key))
            res = await self.db_session.execute(query)
            return res.scalar()

    async def update_param(self, key: str, value: float) -> AppSetting | None:
        async with self.db_session.begin():
            query = (
                update(AppSetting)
                .where(AppSetting.key == key)
                .values(value=value)
                .returning(AppSetting)
            )
            res = await self.db_session.execute(query)
            await self.db_session.commit()
            return res.scalar_one_or_none()

    async def create_param(self, key: str, value: float) -> AppSetting:
        async with self.db_session.begin():
            new_param = AppSetting(key=key, value=value)
            self.db_session.add(new_param)
            await self.db_session.commit()
            return new_param

    @cached(key_builder=lambda db_session, key: build_key(key))
    async def get_param(self, key: str) -> AppSetting | None:
        async with self.db_session.begin():
            query = select(AppSetting).where(AppSetting.key == key)
            res = await self.db_session.execute(query)
            return res.scalar_one_or_none()
    
    async def delete_param(self, id: int) -> AppSetting | None:
        async with self.db_session.begin():
            query = delete(AppSetting).where(AppSetting.id == id).returning(AppSetting)
            deleted_AppSetting = await self.db_session.execute(query)
            await self.db_session.commit()
            return deleted_AppSetting.scalar_one_or_none()