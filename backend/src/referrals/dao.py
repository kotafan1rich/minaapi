from typing import List

from sqlalchemy import delete, exists, select
from sqlalchemy.exc import IntegrityError
from src.cache.redis import build_key, cached
from src.db.dao import BaseDAO
from src.referrals.exceptions import CreateReferralException, UserAlreadyHasReferralsException
from src.referrals.models import Referral


class ReferralDAO(BaseDAO):
    async def create_referral(self, id_from: int, id_to: int):
        async with self.db_session.begin():
            new_referral = Referral(id_from=id_from, id_to=id_to)
            if self.referral_exists(id_to=id_from):
                raise UserAlreadyHasReferralsException()
            try:
                self.db_session.add(new_referral)
                await self.db_session.commit()
            except IntegrityError:
                raise CreateReferralException()
            print(new_referral)
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

    async def get_all_referrals(self, offset: int, limit: int) -> List[Referral | None]:
        async with self.db_session.begin():
            query = select(Referral).offset(offset).limit(limit)
            result = await self.db_session.execute(query)
            return result.scalars().all()

    async def delete_referral(self, id: int) -> Referral | None:
        async with self.db_session.begin():
            query = delete(Referral).where(Referral.id == id).returning(Referral)
            deleted_referral = await self.db_session.execute(query)
            await self.db_session.commit()
            return deleted_referral.scalar_one_or_none()
