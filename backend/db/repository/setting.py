from sqlalchemy.orm import Session
from db.models.setting import Setting
from schemas.setting import SettingCreate, SettingUpdate

def read_all_settings_db(db: Session):
    """ READ all settings. """
    return db.query(Setting).all()

def read_setting_by_slug_db(setting_slug: str, db: Session):
    """ READ setting by slug. """
    return db.query(Setting).filter(Setting.slug == setting_slug).first()

def create_setting_db(setting: SettingCreate, db: Session):
    """ CREATE setting. """
    db_setting = Setting(name=setting.name, slug=setting.slug, value=setting.value)
    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting

def update_setting_db(setting_id: int, setting: SettingUpdate, db: Session):
    """ UPDATE setting. """
    db_setting = db.query(Setting).filter(Setting.id == setting_id).first()
    if db_setting is None:
        return None
    db_setting.name = setting.name
    db_setting.slug = setting.slug
    db_setting.value = setting.value
    db.commit()
    db.refresh(db_setting)
    return db_setting

def delete_setting_db(setting_id: int, db: Session):
    """ DELETE setting. """
    db_setting = db.query(Setting).filter(Setting.id == setting_id).first()
    if db_setting is None:
        return None
    db.delete(db_setting)
    db.commit()
    return db_setting
