import os
import aiofiles
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import UploadFile

from schemas.user import UserCreate
from db.models.user import User
from core.hashing import Hasher
from core.config import project_settings

def __read_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter_by(email=email).first()

def create_user_db(db: Session, user: UserCreate) -> Optional[User]:
    """ CREATE """
    user_in_db = __read_user_by_email(db, user.email)
    if user_in_db:
        return None
    
    user_obj = User(
        email=user.email,
        tg_tag=user.tg_tag,
        password=Hasher.get_password_hash(user.password),
        is_active=True,
        is_superuser=False
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

def read_user_db(db: Session, email: str) -> Optional[User]:
    """ READ """
    user_in_db = __read_user_by_email(db, email)
    return user_in_db

def delete_user_db(db: Session, email: str) -> bool:
    """ DELETE """
    user_in_db = __read_user_by_email(db, email)
    if user_in_db:
        return False
    db.delete(user_in_db)
    db.commit()
    return True

def update_user_db(db: Session, user: UserCreate) -> Optional[User]:
    """ UPDATE """
    user_in_db = __read_user_by_email(db, user.email)
    if not user_in_db:
        return None
    user_in_db.email = user.email
    user_in_db.tg_tag = user.tg_tag
    user_in_db.password = Hasher.get_password_hash(user.password)
    db.commit()
    db.refresh(user_in_db)
    return user_in_db

async def update_avatar_db(db: Session, user: User, file: UploadFile) -> str:
    """ UPDATE. Avatart (profile picture) """
    contents = await file.read()
    upload_path = project_settings.UPLOAD_PATH
    
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

    file_extension = os.path.splitext(file.filename)[1]
    avatar_filename = f"{user.id}_avatar{file_extension}"
    file_path = os.path.join(upload_path, avatar_filename)

    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(contents)
    
    user.avatar = avatar_filename
    db.commit()
    db.refresh(user)

    return avatar_filename

def read_avatar_db(user: User) -> Optional[str]:
    """ READ. Path to user's avatar."""
    if not user.avatar:
        return None
    file_path = os.path.join(project_settings.UPLOAD_PATH, user.avatar)
    if not os.path.exists(file_path):
        return None
    return file_path