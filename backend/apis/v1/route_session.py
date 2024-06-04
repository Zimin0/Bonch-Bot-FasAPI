from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from db.session import get_db
from db.models.user import User
from db.models.pc import PC
from db.models.time_period import TimePeriod
from db.models.session import PC_Session
from schemas.session import SessionGet, SessionCreate, SessionUpdate
from apis.v1.dependencies import get_current_active_superuser

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@router.get('/sessions', response_model=list[SessionGet])
async def get_all_sessions(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ GET all sessions. """
    all_sessions = db.query(PC_Session).all()
    return all_sessions

@router.get('/session/{session_id}', response_model=SessionGet)
async def get_session_by_id(session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ GET session by ID. """
    db_session = db.query(PC_Session).filter(PC_Session.id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return db_session

@router.post('/session', status_code=status.HTTP_201_CREATED, response_model=SessionGet)
async def create_session(pc_session: SessionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ POST create session. """
    user = db.query(User).filter(User.tg_tag == pc_session.tg_tag).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with the provided tg_tag does not exist.")

    ### Бронируем временные промежутки ###
    pc_in_db = db.query(PC).filter(PC.id == pc_session.computer_id).first()
    if not pc_in_db.ready_to_use:
        raise HTTPException(status_code=400, detail="This PC is not ready for use")
    
    pc_time_periods = db.query(TimePeriod).filter(TimePeriod.computer_id == pc_session.computer_id).all()
    TimePeriod.set_status_to_time_periods(
        db=db,
        time_periods=pc_time_periods,
        status="booked",
        start=pc_session.time_start,
        end=pc_session.time_end
    )
    ######################################

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

# @router.put('/session/{session_id}', response_model=SessionGet)
# async def update_session(session_id: int, session: SessionUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
#     """ UPDATE session. """
#     db_session = db.query(PC_Session).filter(PC_Session.id == session_id).first()
#     if db_session is None:
#         raise HTTPException(status_code=404, detail="Session not found")

#     db_session.time_start = session.time_start
#     db_session.time_end = session.time_end
#     db_session.computer_id = session.computer_id
#     db_session.tg_tag = session.tg_tag

#     db.commit()
#     db.refresh(db_session)
#     return db_session

@router.delete('/session/{session_id}')
async def delete_session(session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ DELETE session. """
    db_session = db.query(PC_Session).filter(PC_Session.id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    ### Освобождаем временные промежутки ###
    pc_time_periods = db.query(TimePeriod).filter(TimePeriod.computer_id == db_session.computer_id).all()
    TimePeriod.set_status_to_time_periods(
        db=db,
        time_periods=pc_time_periods,
        status="free",
        start=db_session.time_start,
        end=db_session.time_end
    )
    ######################################

    db.delete(db_session)
    db.commit()
    return {"detail": f"Session {session_id} was deleted."}
