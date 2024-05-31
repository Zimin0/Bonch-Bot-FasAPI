from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from db.models.time_period import TimePeriod
from schemas.time_period import TimePeriodCreate, TimePeriodUpdate, TimePeriodGet
from db.models.user import User
from apis.v1.dependencies import get_current_active_superuser

router = APIRouter()

@router.get('/admin/time_periods/all', response_model=list[TimePeriodGet])
async def get_all_time_periods(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ GET all time periods. """
    all_time_periods = db.query(TimePeriod).all() 
    return all_time_periods

@router.get('/admin/pc/{computer_id}/time_periods', response_model=list[TimePeriodGet])
async def get_pc_time_periods(computer_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ GET time periods of one pc. """
    all_time_periods = db.query(TimePeriod).filter(TimePeriod.computer_id == computer_id).all()
    return all_time_periods

@router.delete('/admin/pc/{computer_id}/time_periods', status_code=status.HTTP_204_NO_CONTENT)
async def delete_pc_time_periods(computer_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ DELETE all time periods of one pc. """
    db.query(TimePeriod).filter(TimePeriod.computer_id == computer_id).delete()
    db.commit()
    return {"detail": f"All time periods for PC {computer_id} were deleted."}

@router.get("/admin/time_period/{time_period_id}", response_model=TimePeriodGet)
async def get_time_period_by_id(time_period_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ GET time period by ID. """
    db_time_period = db.query(TimePeriod).filter(TimePeriod.id == time_period_id).first()
    if db_time_period is None:
        raise HTTPException(status_code=404, detail="Time period not found")
    return db_time_period

@router.post("/admin/time_period", status_code=status.HTTP_201_CREATED, response_model=TimePeriodGet)
async def create_time_period(time_period: TimePeriodCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ POST create time period. """
    db_time_period = TimePeriod(
        time_start=time_period.time_start,
        time_end=time_period.time_end,
        computer_id=time_period.computer_id
    )
    db.add(db_time_period)
    db.commit()
    db.refresh(db_time_period)
    return db_time_period

@router.put("/admin/time_period/{time_period_id}", status_code=status.HTTP_200_OK, response_model=TimePeriodGet)
async def update_time_period(time_period_id: int, time_period: TimePeriodUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ UPDATE time period. """
    db_time_period = db.query(TimePeriod).filter(TimePeriod.id == time_period_id).first()
    if db_time_period is None:
        raise HTTPException(status_code=404, detail="Time period not found")
    db_time_period.time_start = time_period.time_start
    db_time_period.time_end = time_period.time_end
    db_time_period.computer_id = time_period.computer_id
    db.commit()
    db.refresh(db_time_period)
    return db_time_period

@router.delete("/admin/time_period/{time_period_id}")
async def delete_time_period(time_period_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ DELETE time period. """
    db_time_period = db.query(TimePeriod).filter(TimePeriod.id == time_period_id).first()
    if db_time_period is None:
        raise HTTPException(status_code=404, detail="Time period not found")
    db.delete(db_time_period)
    db.commit()
    return {"detail": f"Time period {time_period_id} was deleted."}
