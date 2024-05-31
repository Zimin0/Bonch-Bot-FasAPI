from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session

from db.session import get_db
from db.models.user import User
from schemas.pc import PCGet, PCCreate
from db.models.pc import PC 
from apis.v1.dependencies import get_current_active_superuser


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@router.get('/pc', response_model=list[PCGet])
async def get_all_pc(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ GET all PCs. """
    all_pcs = db.query(PC).all()
    return all_pcs

@router.post('/pc', status_code=status.HTTP_201_CREATED)
async def create_pc(pc: PCCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ POST create session. """
    db_pc = PC(physical_number=pc.physical_number, ready_to_use=pc.ready_to_use)
    db.add(db_pc)
    db.commit()
    db.refresh(db_pc)
    return db_pc