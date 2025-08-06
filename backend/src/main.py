from fastapi import APIRouter, FastAPI
from src.admins.router import admin_router
from src.app_settings.router import app_setting_router
from src.orders.router import order_router
from src.promos.router import promo_router
from src.referrals.router import referral_router
from src.users.router import user_router

app = FastAPI(title="MinatovarAPI")

api_router = APIRouter(prefix="/api")

api_router.include_router(promo_router)
api_router.include_router(user_router)
api_router.include_router(referral_router)
api_router.include_router(order_router)
api_router.include_router(admin_router)
api_router.include_router(app_setting_router)

app.include_router(api_router)
