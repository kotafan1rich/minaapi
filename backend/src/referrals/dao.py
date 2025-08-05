from sqlalchemy import exists, select
from src.cache.redis import build_key, cached
from src.db.dao import BaseDAO
from src.referrals.models import Referral


class ReferralDAO(BaseDAO):
    async def create_referral(self, id_from: int, id_to: int):
        async with self.db_session.begin():
            new_referral = Referral(id_from=id_from, id_to=id_to)
            self.db_session.add(new_referral)
            await self.db_session.commit()
            return new_referral

    async def referral_exists(self, id_to: int):
        async with self.db_session.begin():
            query = select(exists().where(Referral.id_to == id_to))
            res = await self.db_session.execute(query)
            return res.scalar()

    @cached(key_builder=lambda db_session, id_from: build_key(id_from))
    async def get_refferals(self, id_from: int):
        async with self.db_session.begin():
            query = select(Referral.id_to).where(Referral.id_from == id_from)
            res = await self.db_session.execute(query)
            return res.scalars().all()
