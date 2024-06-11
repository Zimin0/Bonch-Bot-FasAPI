from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.time_period import TimePeriodCreate, TimePeriodUpdate, TimePeriodGet
from db.models.user import User
from apis.v1.dependencies import get_current_active_superuser, get_current_active_user
from db.repository.time_period import (
    read_all_time_periods_db,
    read_pc_time_periods_db,
    delete_pc_time_periods_db,
    read_time_period_by_id_db,
    create_time_period_db,
    update_time_period_db,
    delete_time_period_db,
)

router = APIRouter()

@router.get('/admin/time_periods/all', response_model=list[TimePeriodGet])
async def get_all_time_periods(db: Session = Depends(get_db)):
    """ GET all time periods. """
    return read_all_time_periods_db(db)

@router.get('/admin/pc/{computer_id}/time_periods', response_model=list[TimePeriodGet])
async def get_pc_time_periods(computer_id: int, db: Session = Depends(get_db)):
    """ GET time periods of one pc. """
    return read_pc_time_periods_db(computer_id, db)

@router.delete('/admin/pc/{computer_id}/time_periods', status_code=status.HTTP_204_NO_CONTENT)
async def delete_pc_time_periods(computer_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ DELETE all time periods of one pc. """
    delete_pc_time_periods_db(computer_id, db)
    return {"detail": f"All time periods for PC {computer_id} were deleted."}

@router.get("/admin/time_period/{time_period_id}", response_model=TimePeriodGet)
async def get_time_period_by_id(time_period_id: int, db: Session = Depends(get_db)):
    """ GET time period by ID. """
    db_time_period = read_time_period_by_id_db(time_period_id, db)
    if db_time_period is None:
        raise HTTPException(status_code=404, detail="Time period not found")
    return db_time_period

@router.post("/admin/time_period", status_code=status.HTTP_201_CREATED, response_model=TimePeriodGet)
async def create_time_period(time_period: TimePeriodCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ POST create time period. """
    return create_time_period_db(time_period, db)

@router.put("/admin/time_period/{time_period_id}", status_code=status.HTTP_200_OK, response_model=TimePeriodGet)
async def update_time_period(time_period_id: int, time_period: TimePeriodUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ UPDATE time period. """
    db_time_period = update_time_period_db(time_period_id, time_period, db)
    if db_time_period is None:
        raise HTTPException(status_code=404, detail="Time period not found")
    return db_time_period

@router.delete("/admin/time_period/{time_period_id}")
async def delete_time_period(time_period_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ DELETE time period. """
    db_time_period = delete_time_period_db(time_period_id, db)
    if db_time_period is None:
        raise HTTPException(status_code=404, detail="Time period not found")
    return {"detail": f"Time period {db_time_period.time_start}"}
