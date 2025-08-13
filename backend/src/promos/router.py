from fastapi import APIRouter, Depends, HTTPException, status
from src.db.session import get_db
from src.promos.dao import PromoDAO
from src.promos.schemas import ListPromos, ResponsePromo

promo_router = APIRouter(prefix="/promos", tags=["Promos"])


@promo_router.post(path="/create_promo")
async def create_promo(description: str, db_session=Depends(get_db)) -> ResponsePromo:
    if description:
        promo_dao = PromoDAO(db_session=db_session)
        created_promo = await promo_dao.create_promo(description=description)
        if created_promo:
            return ResponsePromo.model_validate(created_promo)
    else:
        raise HTTPException(status_code=422, detail="Not valide description")


@promo_router.delete("/delete_promo")
async def delete_promo(id: int, db_session=Depends(get_db)) -> ResponsePromo:
    promo_dao = PromoDAO(db_session=db_session)
    deleted_promo = await promo_dao.delete_promo(id=id)
    if deleted_promo:
        return ResponsePromo.model_validate(deleted_promo)


@promo_router.get(path="/get_promo")
async def get_promo(id: int, db_session=Depends(get_db)) -> ResponsePromo:
    promo_dao = PromoDAO(db_session=db_session)
    promo = await promo_dao.get_promo(id=id)
    if promo is not None:
        return ResponsePromo.model_validate(promo)
    else:
        raise HTTPException(status_code=404, detail="Promo not found")


@promo_router.get("/get_promos_list")
async def get_promos_list(
    offset: int = 0, limit: int = 10, db_session=Depends(get_db)
) -> ListPromos:
    promo_dao = PromoDAO(db_session=db_session)
    promo_list = await promo_dao.get_all_promos_no_cache(offset=offset, limit=limit)
    if not promo_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Promos not found"
        )
    return ListPromos(
        results=[ResponsePromo.model_validate(promo) for promo in promo_list]
    )
