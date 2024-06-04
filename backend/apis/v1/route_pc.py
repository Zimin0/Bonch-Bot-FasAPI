from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from db.session import get_db
from db.models.user import User
from schemas.pc import PCGet, PCCreate, PCUpdate
from db.models.pc import PC
from apis.v1.dependencies import get_current_active_superuser

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@router.get('/pc/all', response_model=list[PCGet])
async def get_all_pc(db: Session = Depends(get_db)):
    """ GET all PCs. """
    all_pcs = db.query(PC).all()
    return all_pcs

@router.post('/pc', status_code=status.HTTP_201_CREATED, response_model=PCGet)
async def create_pc(pc: PCCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ POST create PC. """
    db_pc = PC(physical_number=pc.physical_number, ready_to_use=pc.ready_to_use)
    db.add(db_pc)
    db.commit()
    db.refresh(db_pc)
    return db_pc

@router.get('/pc/{pc_id}', response_model=PCGet)
async def get_pc_by_id(pc_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ GET PC by ID. """
    db_pc = db.query(PC).filter(PC.id == pc_id).first()
    if db_pc is None:
        raise HTTPException(status_code=404, detail="PC not found")
    return db_pc

@router.put('/pc/{pc_id}', response_model=PCGet)
async def update_pc(pc_id: int, pc: PCUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ UPDATE PC. """
    db_pc = db.query(PC).filter(PC.id == pc_id).first()
    if db_pc is None:
        raise HTTPException(status_code=404, detail="PC not found")
    db_pc.physical_number = pc.physical_number
    db_pc.ready_to_use = pc.ready_to_use
    db.commit()
    db.refresh(db_pc)
    return db_pc

@router.delete('/pc/{pc_id}')
async def delete_pc(pc_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ DELETE PC. """
    db_pc = db.query(PC).filter(PC.id == pc_id).first()
    if db_pc is None:
        raise HTTPException(status_code=404, detail="PC not found")
    db.delete(db_pc)
    db.commit()
    return {"detail": f"PC {pc_id} was deleted."}
