from sqlalchemy.orm import Session
from db.models.time_period import TimePeriod
from schemas.time_period import TimePeriodCreate, TimePeriodUpdate

def read_all_time_periods_db(db: Session):
    """ READ all time periods. """
    return db.query(TimePeriod).all()

def read_pc_time_periods_db(pc_physical_number: int, db: Session):
    """ READ time periods of one pc. """
    return db.query(TimePeriod).filter(TimePeriod.computer_id == pc_physical_number).order_by(TimePeriod.time_start).all()

def delete_pc_time_periods_db(computer_id: int, db: Session):
    """ DELETE all time periods of one pc. """
    db.query(TimePeriod).filter(TimePeriod.computer_id == computer_id).delete()
    db.commit()

def read_time_period_by_id_db(time_period_id: int, db: Session):
    """ READ time period by ID. """
    return db.query(TimePeriod).filter(TimePeriod.id == time_period_id).first()

def create_time_period_db(time_period: TimePeriodCreate, db: Session):
    """ CREATE time period. """
    db_time_period = TimePeriod(
        time_start=time_period.time_start,
        time_end=time_period.time_end,
        computer_id=time_period.computer_id,
        status=time_period.status
    )
    db.add(db_time_period)
    db.commit()
    db.refresh(db_time_period)
    return db_time_period

def update_time_period_db(time_period_id: int, time_period: TimePeriodUpdate, db: Session):
    """ UPDATE time period. """
    db_time_period = db.query(TimePeriod).filter(TimePeriod.id == time_period_id).first()
    if db_time_period is None:
        return None
    db_time_period.time_start = time_period.time_start
    db_time_period.time_end = time_period.time_end
    db_time_period.computer_id = time_period.computer_id
    db_time_period.status = time_period.status
    db.commit()
    db.refresh(db_time_period)
    return db_time_period

def delete_time_period_db(time_period_id: int, db: Session):
    """ DELETE time period. """
    db_time_period = db.query(TimePeriod).filter(TimePeriod.id == time_period_id).first()
    if db_time_period is None:
        return None
    db.delete(db_time_period)
    db.commit()
    return db_time_period
