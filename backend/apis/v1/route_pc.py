from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from db.session import get_db
from db.repository.pc import read_pc_all_db, create_pc_db, read_pc_by_physical_number_db, update_pc_db, delete_pc_db
from db.models.user import User
from schemas.pc import PCGet, PCCreate
from apis.v1.dependencies import get_current_active_superuser

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@router.get('/pc/all', response_model=list[PCGet])
async def get_all_pc(db: Session = Depends(get_db)):
    """ GET all PCs. """
    all_pcs = read_pc_all_db(db=db)
    return all_pcs

@router.post('/pc', status_code=status.HTTP_201_CREATED, response_model=PCGet)
async def create_pc(pc: PCCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ POST create PC. """
    pc_in_db = create_pc_db(db=db, pc=pc)
    if not pc_in_db:
        raise HTTPException(status_code=404, detail="PC already exists.")
    return pc_in_db

@router.get('/pc/{physical_number}', response_model=PCGet)
async def get_pc(physical_number: int, db: Session = Depends(get_db)):
    """ GET PC by physical_number. """
    db_pc = read_pc_by_physical_number_db(db=db, id=physical_number)
    if db_pc is None:
        raise HTTPException(status_code=404, detail="PC not found.")
    return db_pc

@router.put('/pc/{pc_id}', response_model=PCGet)
async def update_pc(pc_id: int, pc: PCCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ UPDATE PC. """
    db_pc = update_pc_db(db=db, pc=pc) 
    if db_pc is None:
        raise HTTPException(status_code=404, detail="PC not found.")
    return db_pc

@router.delete('/pc/{physical_number}')
async def delete_pc(physical_number: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ DELETE PC. """
    db_pc = delete_pc_db(db=db, physical_number=physical_number)
    if db_pc is None:
        raise HTTPException(status_code=404, detail="PC not found.")
    return {"detail": f"PC {physical_number} was deleted."}
