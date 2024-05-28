from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter, Request
from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from db.session import get_db
from core.hashing import Hasher
from schemas.token import Token
from db.repository.user import get_user
from core.security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
templates = Jinja2Templates(directory="templates")

@router.get('/login', response_class=HTMLResponse)
async def show_login_page(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("auth/login.html", {'request':request})

@router.get('/register', response_class=HTMLResponse)
async def show_register_page(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse('auth/register.html', {'request': request})

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}

def authenticate_user(email: str, password: str,db: Session):
    user = get_user(email=email,db=db)
    print(user)
    if not user:
        return False
    if not Hasher.verify_password(password, user.password):
        return False
    return user