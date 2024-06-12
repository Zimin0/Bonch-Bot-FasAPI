from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.setting import SettingCreate, SettingUpdate, SettingGet
from db.models.user import User
from apis.v1.dependencies import get_current_active_superuser
from db.repository.setting import (
    read_all_settings_db,
    read_setting_by_slug_db,
    create_setting_db,
    update_setting_db,
    delete_setting_db
)

router = APIRouter()

@router.get('/settings/all', response_model=list[SettingGet])
async def get_all_settings(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ GET all settings. """
    return read_all_settings_db(db)

@router.get("/setting/slug/{setting_slug}")
async def get_setting_by_slug(setting_slug: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ GET setting by slug. """
    db_setting = read_setting_by_slug_db(setting_slug, db)
    if db_setting is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    return db_setting

@router.post("/setting", status_code=status.HTTP_201_CREATED)
async def create_setting(setting: SettingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ POST create setting. """
    return create_setting_db(setting, db)

@router.put("/setting/{setting_id}", status_code=status.HTTP_201_CREATED)
async def update_setting(setting_id: int, setting: SettingUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ UPDATE setting. """
    db_setting = update_setting_db(setting_id, setting, db)
    if db_setting is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    return db_setting

@router.delete("/setting/{setting_id}")
async def delete_setting(setting_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ DELETE setting. """
    db_setting = delete_setting_db(setting_id, db)
    if db_setting is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    return {"detail": f"Setting {setting_id} was deleted."}
