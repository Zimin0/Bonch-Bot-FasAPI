from fastapi import APIRouter, status, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db.session import get_db
from db.models.setting import Setting
from schemas.setting import SettingCreate, SettingUpdate
from db.models.user import User

from apis.v1.dependencies import get_current_active_superuser

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/admin/settings", response_class=HTMLResponse)
async def read_settings(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    settings = db.query(Setting).all()
    return templates.TemplateResponse("settings.html", {"request": request, "settings": settings})

@router.get("/admin/settings/slug/{setting_slug}")
async def get_setting_by_slug(setting_slug: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    db_setting = db.query(Setting).filter(Setting.slug == setting_slug).first()
    if db_setting is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    return db_setting

@router.post("/admin/settings")
async def create_setting(setting: SettingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    db_setting = Setting(name=setting.name, slug=setting.slug, value=setting.value)
    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting

@router.put("/admin/settings/{setting_id}")
async def update_setting(setting_id: int, setting: SettingUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    db_setting = db.query(Setting).filter(Setting.id == setting_id).first()
    if db_setting is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    db_setting.name = setting.name
    db_setting.slug = setting.slug  
    db_setting.value = setting.value
    db.commit()
    db.refresh(db_setting)
    return db_setting

@router.delete("/admin/settings/{setting_id}")
async def delete_setting(setting_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    db_setting = db.query(Setting).filter(Setting.id == setting_id).first()
    if db_setting is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    db.delete(db_setting)
    db.commit()
    return {"detail": f"Setting {setting_id} was deleted."}
