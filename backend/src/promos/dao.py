from typing import List
from sqlalchemy import delete, select
from src.cache.redis import build_key, cached
from src.db.dao import BaseDAO
from src.promos.models import Promo


class PromoDAO(BaseDAO):
    @cached(key_builder=lambda db_session: build_key("promo"))
    async def get_all_promos(self) -> List[Promo | None]:
        async with self.db_session.begin():
            query = select(Promo).order_by(Promo.id)
            result = await self.db_session.execute(query)
            return result.scalars().all()
    
    async def get_all_promos_no_cache(self, offset: int, limit: int) -> List[Promo | None]:
        async with self.db_session.begin():
            query = select(Promo).offset(offset).limit(limit).order_by(Promo.id)
            result = await self.db_session.execute(query)
            return result.scalars().all()

    async def create_promo(self, description: str) -> Promo:
        async with self.db_session.begin():
            new_promo = Promo(description=description)
            self.db_session.add(new_promo)
            await self.db_session.commit()
            return new_promo

    async def get_promo(self, id: int) -> Promo | None:
        async with self.db_session.begin():
            query = select(Promo).where(Promo.id == id)
            result = await self.db_session.execute(query)
            return result.scalar_one_or_none()

    async def delete_promo(self, id: int) -> Promo | None:
        async with self.db_session.begin():
            query = delete(Promo).where(Promo.id == id).returning(Promo)
            deleted_promo = await self.db_session.execute(query)
            await self.db_session.commit()
            return deleted_promo.scalar_one_or_none()
