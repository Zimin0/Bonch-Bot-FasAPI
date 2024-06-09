from fastapi import APIRouter, status, Depends, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from schemas.user import UserCreate, UserGet
from db.models.user import User
from db.session import get_db
from apis.v1.dependencies import get_current_active_superuser, get_current_user
from db.repository.user import create_new_user, read_user, delete_user, update_user, update_avatar, read_avatar_path

router = APIRouter()

@router.get('/user/me', response_model=UserGet)
async def get_my_info(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """ GET. Возвращает информацию о себе. """
    response_obj = UserGet.model_validate(current_user) # Метод model_validate служит для преобразования ORM модели в объект схемы Pydantic, выполняя валидацию данных в процессе.
    return response_obj

@router.get("/user/email/{email}", response_model=UserGet)
async def user_by_email(email:str, db: Session = Depends(get_db)):
    """ GET. Возвращает информацию о пользователе по электронной почте. """
    user_in_db = read_user(db=db, email=email)
    if not user_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_in_db

@router.post('/user', response_model=UserGet, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser),):
    """ POST """
    user_in_db = create_new_user(db=db, user=user_in_db)
    if not user_in_db: # пользователь уже существует
        raise HTTPException(status_code=400, detail="Such a user already exists.")
    return user_in_db

@router.put('/user', response_model=UserGet, status_code=status.HTTP_201_CREATED)
def update_user(user_request: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """ PUT """
    user_in_db = update_user(db=db, user=user_request)
    if not user_in_db: # пользователь не найден
        raise HTTPException(status_code=404, detail="User not found")
    return user_in_db

@router.delete('/user', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_account(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """ DELETE """
    user_in_db = delete_user(db=db, email=current_user.email)
    if not user_in_db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted."}

@router.post("/user/avatar")
async def upload_my_avatar(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """ POST. Загружает аватар пользователя. """
    try:
        avatar_filename = await update_avatar(db=db, user=current_user, file=file)
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"There was an error uploading your avatar: {e}")
    finally:
        await file.close()

    return {"detail": "New avatar was uploaded."}

@router.get('/user/avatar', response_class=FileResponse)
async def get_my_avatar(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """ GET. Получает аватар пользователя. """
    file_path = read_avatar_path(current_user)
    if not file_path:
        raise HTTPException(status_code=404, detail="User's avatar not found.")
    return FileResponse(file_path)