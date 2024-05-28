from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from core.config import settings
from db.session import get_db
from db.models.user import User
from db.repository.user import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """ Возвращает пользователя по токену. """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверные данные для входа.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        print(f"{username=}")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user(email=username, db=db)
    if user is None:
        raise credentials_exception
    
    print(f"User: {user.email}, is_active: {user.is_active}, is_superuser: {user.is_superuser}")
    
    return user

def get_current_active_superuser(current_user: User = Depends(get_current_user)) -> User:
    """ Проверяет, является ли пользователь superuser'ом. """
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="The user doesn't have enough privileges")
    print(f"User \"{current_user.email}\" is superuser.")
    return current_user
