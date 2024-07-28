from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from db.models.session import PC_Session
from db.repository.session import read_session_time_periods
from apis.business_logic.session_creation_rules import SessionValidator
from db.session import get_db
from db.models.user import User
from schemas.session import SessionGet, SessionCreate
from apis.v1.dependencies import get_current_active_superuser
from db.repository.session import (
    read_all_sessions_db,
    read_session_by_id_db,
    create_session_db,
    delete_session_db
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@router.get('/sessions', response_model=list[SessionGet])
async def get_all_sessions(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ GET all sessions. """
    return read_all_sessions_db(db)

@router.get('/session/{session_id}', response_model=SessionGet)
async def get_session_by_id(session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ GET session by ID. """
    db_session = read_session_by_id_db(session_id, db)
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return db_session

@router.get('/user_sessions', response_model=list[SessionGet])
async def get_user_sessions(current_user: User = Depends(get_current_active_superuser), db: Session = Depends(get_db)):
    """ GET all sessions for the current user. """
    user_sessions = db.query(PC_Session).filter(PC_Session.tg_tag == current_user.tg_tag).all()
    return user_sessions

@router.post('/session', status_code=status.HTTP_201_CREATED, response_model=SessionGet)
async def create_session(pc_session: SessionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ POST create session. """
    validator = SessionValidator()
    session_time_periods = read_session_time_periods(db, pc_session)
    validation_results = validator.validate(pc_session, session_time_periods)
    print(validation_results)
    if validation_results:
        error_message = ";\n".join(validation_results)
        raise HTTPException(status_code=400, detail=error_message)
    db_session = create_session_db(pc_session, db)
    if db_session is None:
        raise HTTPException(status_code=404, detail="User or PC not found or PC not ready for use")
    return db_session

@router.delete('/session/{session_id}')
async def delete_session(session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ DELETE session. """
    db_session = delete_session_db(session_id, db)
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"detail": f"Session {session_id} was deleted."}
