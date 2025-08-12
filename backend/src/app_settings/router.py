from fastapi import APIRouter, Depends

from src.app_settings.dao import AppSettingDAO
from src.app_settings.schemas import ResponseSetting
from src.db.session import get_db


app_setting_router = APIRouter(prefix="/app_settings", tags=["App Settings"])

@app_setting_router.post("/create_setting", response_model=ResponseSetting)
async def create_setting(key: str, value: float, db_session=Depends(get_db)):
    setting_dao = AppSettingDAO(db_session=db_session)
    created_setting = await setting_dao.create_param(key=key, value=value)
    if created_setting:
        return ResponseSetting.model_validate(created_setting, from_attributes=True)


@app_setting_router.delete("/delete_setting", response_model=ResponseSetting)
async def delete_setting(id: int, db_session=Depends(get_db)):
    settings_dao = AppSettingDAO(db_session=db_session)
    deleted_setting = await settings_dao.delete_param(id=id)
    if deleted_setting:
        return ResponseSetting.model_validate(deleted_setting, from_attributes=True)


@app_setting_router.get("/get_setting", response_model=ResponseSetting)
async def get_setting(key: str, db_session=Depends(get_db)):
    setting_dao = AppSettingDAO(db_session=db_session)
    setting = await setting_dao.get_param(key=key)
    if setting:
        return ResponseSetting.model_validate(setting, from_attributes=True)


@app_setting_router.patch("/update_setting", response_model=ResponseSetting)
async def update_setting(key: str, value: float, db_session=Depends(get_db)):
    setting_dao = AppSettingDAO(db_session=db_session)
    updated_setting = await setting_dao.update_param(key=key, value=value)
    if updated_setting:
        return ResponseSetting.model_validate(updated_setting, from_attributes=True)
