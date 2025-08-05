from fastapi import APIRouter, Depends

from src.db.session import get_db
from src.referrals.dao import ReferralDAO
from src.referrals.schemas import ListReferrals, ResponseReferral


referral_router = APIRouter(prefix="/referrals", tags=["Referrals"])

@referral_router.post("/create_referral", response_model=ResponseReferral)
async def create_referral(id_from: int, id_to: int, db_session=Depends(get_db)):
    referral_dao = ReferralDAO(db_session=db_session)
    created_referral = await referral_dao.create_referral(id_from=id_from, id_to=id_to)
    if created_referral:
        return ResponseReferral.model_validate(created_referral, from_attributes=True)


@referral_router.get("/get_referrals", response_model=ListReferrals)
async def get_referrals(id_from: int, db_session=Depends(get_db)):
    referral_dao = ReferralDAO(db_session=db_session)
    result =await referral_dao.get_refferals(id_from=id_from)
    if result:
        return ListReferrals(result=result)

