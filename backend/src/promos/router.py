from fastapi import APIRouter, Depends, HTTPException

from src.db.session import get_db
from src.promos.dao import PromoDAO
from src.promos.schemas import ResponsePromo


promo_router = APIRouter(prefix="/promos", tags=["Promos"])


@promo_router.post(path="/create_promo", response_model=ResponsePromo)
async def create_promo(description: str, db_session=Depends(get_db)):
    if description:
        promo_dao = PromoDAO(db_session=db_session)
        created_promo = await promo_dao.create_promo(description=description)
        if created_promo:
            return ResponsePromo.model_validate(created_promo, from_attributes=True)
    else:
        raise HTTPException(status_code=422, detail="Not valide description")


@promo_router.get(path="/get_promo", response_model=ResponsePromo)
async def get_promo(id: int, db_session=Depends(get_db)):
    promo_dao = PromoDAO(db_session=db_session)
    promo = await promo_dao.get_promo(id=id)
    if promo is not None:
        return ResponsePromo.model_validate(promo, from_attributes=True)
    else:
        raise HTTPException(status_code=404, detail="Promo not found")
