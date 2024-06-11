from sqlalchemy.orm import Session
from db.models.session import PC_Session
from schemas.session import SessionCreate, SessionUpdate
from db.models.user import User
from db.models.pc import PC
from db.models.time_period import TimePeriod

def read_all_sessions_db(db: Session):
    """ READ all sessions. """
    return db.query(PC_Session).all()

def read_session_by_id_db(session_id: int, db: Session):
    """ READ session by ID. """
    return db.query(PC_Session).filter(PC_Session.id == session_id).first()

def create_session_db(pc_session: SessionCreate, db: Session):
    """ CREATE session. """
    user = db.query(User).filter(User.tg_tag == pc_session.tg_tag).first()
    if not user:
        return None

    pc_in_db = db.query(PC).filter(PC.id == pc_session.computer_id).first()
    if not pc_in_db.ready_to_use:
        return None

    pc_time_periods = db.query(TimePeriod).filter(TimePeriod.computer_id == pc_session.computer_id).all()
    TimePeriod.set_status_to_time_periods(
        db=db,
        time_periods=pc_time_periods,
        status="booked",
        start=pc_session.time_start,
        end=pc_session.time_end
    )

    db_pc_session = PC_Session(
        time_start=pc_session.time_start,
        time_end=pc_session.time_end,
        computer_id=pc_session.computer_id,
        tg_tag=pc_session.tg_tag
    )
    db.add(db_pc_session)
    db.commit()
    db.refresh(db_pc_session)
    return db_pc_session

def delete_session_db(session_id: int, db: Session):
    """ DELETE session. """
    db_session = db.query(PC_Session).filter(PC_Session.id == session_id).first()
    if db_session is None:
        return None

    pc_time_periods = db.query(TimePeriod).filter(TimePeriod.computer_id == db_session.computer_id).all()
    TimePeriod.set_status_to_time_periods(
        db=db,
        time_periods=pc_time_periods,
        status="free",
        start=db_session.time_start,
        end=db_session.time_end
    )

    db.delete(db_session)
    db.commit()
    return db_session
