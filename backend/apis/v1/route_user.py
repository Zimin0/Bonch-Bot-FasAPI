from fastapi import APIRouter, status, Depends, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from schemas.user import UserCreate, UserGet
from db.models.user import User
from db.session import get_db
from apis.v1.dependencies import get_current_active_superuser, get_current_user
from db.repository.user import create_user_db, read_user_db, delete_user_db, update_user_db, update_avatar_db, read_avatar_db

router = APIRouter()

@router.get('/user/me', response_model=UserGet)
async def get_my_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """ GET. Возвращает информацию о себе. """
    response_obj = UserGet.model_validate(current_user) # Метод model_validate служит для преобразования ORM модели в объект схемы Pydantic, выполняя валидацию данных в процессе.
    print(response_obj)
    return response_obj

@router.get("/user/{email}", response_model=UserGet)
async def get_user(email:str, db: Session = Depends(get_db)):
    """ GET. Возвращает информацию о пользователе по электронной почте. """
    user_in_db = read_user_db(db=db, email=email)
    if not user_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_in_db

@router.post('/user', response_model=UserGet, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser),):
    """ POST """
    user_in_db = create_user_db(db=db, user=user_in_db)
    if not user_in_db: # пользователь уже существует
        raise HTTPException(status_code=400, detail="User already exists.")
    return user_in_db

@router.put('/user', response_model=UserGet, status_code=status.HTTP_201_CREATED)
def update_user(user_request: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """ PUT """
    user_in_db = update_user_db(db=db, user=user_request)
    if not user_in_db: # пользователь не найден
        raise HTTPException(status_code=404, detail="User not found")
    return user_in_db

@router.delete('/user', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """ DELETE """
    user_in_db = delete_user_db(db=db, email=current_user.email)
    if not user_in_db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted."}

@router.get('/user/avatar/me', response_class=FileResponse)
async def get_my_avatar(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """ GET. Получает аватар пользователя. """
    file_path = read_avatar_db(current_user)
    if not file_path:
        raise HTTPException(status_code=404, detail="User's avatar not found.")
    print(file_path)
    return FileResponse(file_path)

@router.post("/user/avatar")
async def upload_my_avatar(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """ POST. Загружает аватар пользователя. """
    try:
        await update_avatar_db(db=db, user=current_user, file=file)
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"There was an error uploading your avatar: {error}")
    finally:
        await file.close()

    return {"detail": "New avatar was uploaded."}
