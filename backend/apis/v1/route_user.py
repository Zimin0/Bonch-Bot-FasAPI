from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import File, UploadFile
from core.config import project_settings
import os
import aiofiles
from fastapi.responses import FileResponse

from schemas.user import UserCreate, ShowUser
from db.session import get_db
from db.models.user import User
from db.repository.user import create_new_user
from apis.v1.dependencies import get_current_active_superuser, get_current_user
from db.repository.user import create_new_user, get_user, delete_user
from core.hashing import Hasher

router = APIRouter()

@router.post('/user', response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db),  current_user: User = Depends(get_current_active_superuser),):
    user = create_new_user(user=user, db=db)
    return user

@router.put('/user', response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def update_user(user_request: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_in_db = get_user(db=db, email=user_request.email)
    if not user_in_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_in_db.email = user_request.email
    user_in_db.tg_tag = user_request.tg_tag
    user_in_db.password = Hasher.get_password_hash(user_request.password)
    db.commit()
    db.refresh(user_in_db)

    return user_in_db

@router.delete('/user', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_account(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = get_user(email=current_user.email, db=db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    delete_user(user, db)
    return {"detail": "User deleted."}

@router.get('/user/me', response_model=ShowUser)
async def get_my_info(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Возвращает информацию о себе. """
    response_obj = ShowUser.model_validate(current_user)
    # user_me = db.query(User).filter(User.id == user_id).first()
    return response_obj

@router.post("/user/avatar")
async def upload_my_avatar(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        contents = await file.read()
        upload_path = project_settings.UPLOAD_PATH
        
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)

        file_extension = os.path.splitext(file.filename)[1]
        avatar_filename = f"{current_user.id}_avatar{file_extension}"
        file_path = os.path.join(upload_path, avatar_filename)

        print(file_path)
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(contents)
        
        current_user.avatar = avatar_filename
        db.commit()
        db.refresh(current_user)
    except Exception as e:
        return {"message": f"There was an error uploading your avatar: {e}"}
    finally:
        await file.close()

    return {"detail": "New avatar was uploaded."}


@router.get('/user/avatar', response_class=FileResponse)
async def get_my_avatar(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.avatar:
        raise HTTPException(status_code=404, detail="Avatar not found")
    
    file_path = os.path.join(project_settings.UPLOAD_PATH, current_user.avatar)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Avatar not found")
    
    return FileResponse(file_path)