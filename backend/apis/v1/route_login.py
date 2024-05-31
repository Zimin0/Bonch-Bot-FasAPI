from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends, APIRouter, Request
from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from db.session import get_db
from core.hashing import Hasher
from schemas.token import Token
from db.repository.user import get_user
from core.security import create_access_token
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from schemas.user import UserCreate, ShowUser
from db.models.user import User
from db.repository.user import create_new_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
# templates = Jinja2Templates(directory="templates")

# @router.get('/login', response_class=HTMLResponse)
# async def show_login_page(request: Request, db: Session = Depends(get_db)):
#     return templates.TemplateResponse("auth/login.html", {'request': request})

# @router.get('/register', response_class=HTMLResponse)
# async def show_register_page(request: Request, db: Session = Depends(get_db)):
#     return templates.TemplateResponse('auth/register.html', {'request': request})

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        print("Такой пользователь уже существует.")
        raise HTTPException(status_code=400, detail="User already exists")
    
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

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(
        data={"sub": user.email}
    )
    print(access_token)
    return {"access_token": access_token, "token_type": "bearer"}

def authenticate_user(email: str, password: str, db: Session):
    user = get_user(email=email, db=db)
    if not user:
        print(f"User with email {email} not found.")
        return False
    if not Hasher.verify_password(password, user.password):
        print(f"Incorrect password for user {email}.")
        return False
    print(f"Authenticated user: {user.email}")
    return user
