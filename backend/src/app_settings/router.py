from fastapi import APIRouter, Depends, HTTPException, status
from src.app_settings.dao import AppSettingDAO
from src.app_settings.schemas import SettingSchema, ResponseSettingsList
from src.db.session import get_db

app_setting_router = APIRouter(prefix="/app_settings", tags=["App Settings"])


@app_setting_router.post("/create_setting")
async def create_setting(
    key: str, value: float, db_session=Depends(get_db)
) -> SettingSchema:
    setting_dao = AppSettingDAO(db_session=db_session)
    created_setting = await setting_dao.create_param(key=key, value=value)
    if created_setting:
        return SettingSchema.model_validate(created_setting)


@app_setting_router.get("/get_settings_list")
async def get_settings_list(
    offset: int = 0, limit: int = 10, db_session=Depends(get_db)
) -> ResponseSettingsList:
    setting_dao = AppSettingDAO(db_session=db_session)
    settings_list = await setting_dao.get_all_params(offset=offset, limit=limit)
    if not settings_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Params not found"
        )
    return ResponseSettingsList(
        results=[SettingSchema.model_validate(setting) for setting in settings_list]
    )


@app_setting_router.delete("/delete_setting")
async def delete_setting(id: int, db_session=Depends(get_db)) -> SettingSchema:
    settings_dao = AppSettingDAO(db_session=db_session)
    deleted_setting = await settings_dao.delete_param(id=id)
    if deleted_setting:
        return SettingSchema.model_validate(deleted_setting)


@app_setting_router.get("/get_setting")
async def get_setting(key: str, db_session=Depends(get_db)) -> SettingSchema:
    setting_dao = AppSettingDAO(db_session=db_session)
    setting = await setting_dao.get_param(key=key)
    if setting:
        return SettingSchema.model_validate(setting)


@app_setting_router.patch("/update_setting")
async def update_setting(
    key: str, value: float, db_session=Depends(get_db)
) -> SettingSchema:
    setting_dao = AppSettingDAO(db_session=db_session)
    updated_setting = await setting_dao.update_param(key=key, value=value)
    if updated_setting:
        return SettingSchema.model_validate(updated_setting)
