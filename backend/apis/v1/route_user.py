from fastapi import APIRouter, status
from sqlalchemy.orm import Session
from fastapi import Depends

from schemas.user import UserCreate, ShowUser
from db.session import get_db
from db.models.user import User
from db.repository.user import create_new_user
from apis.v1.dependencies import get_current_active_superuser

router = APIRouter()

@router.post('/user', response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user

@router.get('/user/me', response_model=ShowUser)
async def get_my_info(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """Возвращает информацию о себе. """
    response_obj = ShowUser.model_validate(current_user)
    # user_me = db.query(User).filter(User.id == user_id).first()
    return response_obj
        