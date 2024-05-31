from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from db.models.user import User
from schemas.session import SessionGet, SessionCreate
from apis.v1.dependencies import get_current_active_superuser
from db.models.session import PC_Session

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@router.get('/session', response_model=list[SessionGet])
async def get_all_sessions(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ GET all sessions. """
    all_sessions = db.query(PC_Session).all()
    return all_sessions

@router.post('/session', status_code=status.HTTP_201_CREATED, response_model=SessionGet)
async def create_session(pc_session: SessionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    """ POST create session. """
    user = db.query(User).filter(User.tg_tag == pc_session.tg_tag).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with the provided tg_tag does not exist.")

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







"""
[
  {
    "id": 0,
    "time_start": "19:24:50.014Z",
    "time_end": "19:24:50.014Z",
    "computer_id": 0
  }
]
"""