from fastapi import APIRouter, Depends, HTTPException, status

from src.db.session import get_db
from src.referrals.dao import ReferralDAO
from src.referrals.exceptions import (
    CreateReferralException,
    UserAlreadyHasReferralsException,
)
from src.referrals.schemas import ListReferrals, ReferralSchema


referral_router = APIRouter(prefix="/referrals", tags=["Referrals"])


@referral_router.post("/create_referral")
async def create_referral(
    id_from: int, id_to: int, db_session=Depends(get_db)
) -> ReferralSchema:
    referral_dao = ReferralDAO(db_session=db_session)
    try:
        created_referral = await referral_dao.create_referral(
            id_from=id_from, id_to=id_to
        )
        return ReferralSchema.model_validate(created_referral)
    except CreateReferralException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Id_from or id_to doesn't exists",
        )
    except UserAlreadyHasReferralsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This user can't be a referral"
        )


@referral_router.delete("/delete_referral")
async def delete_referral(id: int, db_session=Depends(get_db)) -> ReferralSchema:
    referral_dao = ReferralDAO(db_session=db_session)
    deleted_referral = await referral_dao.delete_referral(id=id)
    if deleted_referral:
        return ReferralSchema.model_validate(deleted_referral)


@referral_router.get("/get_referrals")
async def get_referrals(id_from: int, db_session=Depends(get_db)) -> ListReferrals:
    referral_dao = ReferralDAO(db_session=db_session)
    result = await referral_dao.get_refferals(id_from=id_from)
    if result:
        return ListReferrals(result=result)


@referral_router.get("/get_referrals_list")
async def get_referrals_list(
    offset: int = 0, limit: int = 10, db_session=Depends(get_db)
) -> ListReferrals:
    referral_dao = ReferralDAO(db_session=db_session)
    referrals_list = await referral_dao.get_all_referrals(offset=offset, limit=limit)
    if not referrals_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Referrals not found"
        )
    return ListReferrals(
        results=[
            ReferralSchema.model_validate(referral) for referral in referrals_list
        ]
    )
