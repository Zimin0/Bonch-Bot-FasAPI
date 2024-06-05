from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from db.models.setting import Setting
from schemas.setting import SettingCreate, SettingUpdate, SettingGet
from db.models.user import User
from apis.v1.dependencies import get_current_active_superuser, get_current_active_user

router = APIRouter()

@router.get('/admin/settings/all', response_model=list[SettingGet])
async def get_all_settings(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ GET all settings. """
    all_settings = db.query(Setting).all() 
    return all_settings

@router.get("/admin/setting/slug/{setting_slug}")
async def get_setting_by_slug(setting_slug: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ GET setting by slug. """
    db_setting = db.query(Setting).filter(Setting.slug == setting_slug).first()
    if db_setting is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    return db_setting

@router.post("/admin/setting", status_code=status.HTTP_201_CREATED)
async def create_setting(setting: SettingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ POST create setting. """
    db_setting = Setting(name=setting.name, slug=setting.slug, value=setting.value)
    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting

@router.put("/admin/setting/{setting_id}", status_code=status.HTTP_201_CREATED)
async def update_setting(setting_id: int, setting: SettingUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ UPDATE setting. """
    db_setting = db.query(Setting).filter(Setting.id == setting_id).first()
    if db_setting is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    db_setting.name = setting.name
    db_setting.slug = setting.slug  
    db_setting.value = setting.value
    db.commit()
    db.refresh(db_setting)
    return db_setting

@router.delete("/admin/setting/{setting_id}")
async def delete_setting(setting_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ DELETE setting. """
    db_setting = db.query(Setting).filter(Setting.id == setting_id).first()
    if db_setting is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    db.delete(db_setting)
    db.commit()
    return {"detail": f"Setting {setting_id} was deleted."}
