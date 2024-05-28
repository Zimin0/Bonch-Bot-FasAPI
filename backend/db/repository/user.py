from sqlalchemy.orm import Session

from schemas.user import UserCreate
from db.models.user import User
from core.hashing import Hasher

def create_new_user(user: UserCreate, db: Session):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
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

def get_user(email:str, db:Session):
    user = db.query(User).filter(User.email == email).first()
    return user
