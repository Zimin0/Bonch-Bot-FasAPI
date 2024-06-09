from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session

from core.hashing import Hasher
from core.security import create_access_token
from schemas.token import Token
from schemas.user import UserCreate
from db.session import get_db
from db.repository.user import read_user_db
from db.models.user import User
from db.repository.user import create_user_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    user_in_db = create_user_db(db=db, user=user)
    ...
    # Дополнительный функционал - например - подтверждение почты.
    ...
    if not user_in_db:
        raise HTTPException(status_code=400, detail="User already exists.")
    return user_in_db

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = __authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

def __authenticate_user(email: str, password: str, db: Session):
    user = read_user_db(email=email, db=db)
    if not user: # Пользователь не найден
        return False
    if not Hasher.verify_password(password, user.password): # Неверный пароль
        return False
    return user
