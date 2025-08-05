from fastapi import APIRouter, FastAPI
from src.promos.router import promo_router
from src.users.router import user_router
from src.referrals.router import referral_router
from src.orders.router import order_router

app = FastAPI(title="MinatovarAPI")

api_router = APIRouter(prefix="/api")

api_router.include_router(promo_router)
api_router.include_router(user_router)
api_router.include_router(referral_router)
api_router.include_router(order_router)

app.include_router(api_router)
