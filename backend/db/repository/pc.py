from sqlalchemy.orm import Session
from typing import Optional
from typing import Any

from db.models.pc import PC
from schemas.pc import PCCreate

def __read_pc_by_field(db: Session, field_name: str, value: Any) -> Optional[PC]:
    return db.query(PC).filter(getattr(PC, field_name) == value).first() # getattr используется в тех случаях, когда объект и/или имя атрибута может варьироваться (является переменной).

def read_pc_all_db(db: Session) -> list[PC]:
    return db.query(PC).all()

def read_pc_by_physical_number_db(db: Session, physical_number:int) -> Optional[PC]:
    """ READ. by physical_number"""
    pc_in_db = __read_pc_by_field(db=db, field_name="physical_number", value=physical_number)
    return pc_in_db

def create_pc_db(db: Session, pc: PCCreate) -> Optional[PC]:
    """ CREATE """
    pc_in_db = __read_pc_by_field(db=db, field_name="physical_number", value=pc.physical_number)
    if pc_in_db:
        return None
    
    pc_obj = PC(
        physical_number=pc.physical_number,
        ready_to_use=pc.ready_to_use
    )
    db.add(pc_obj)
    db.commit()
    db.refresh(pc_obj)
    return pc_obj

def update_pc_db(db: Session, pc:PCCreate) -> Optional[PC]:
    """ UPDATE """
    pc_in_db = __read_pc_by_field(db=db, field_name="physical_number", value=pc.physical_number)
    if not pc_in_db:
        return None
    
    pc_in_db.physical_number = pc.physical_number
    pc_in_db.ready_to_use = pc.ready_to_use

    db.commit()
    db.refresh(pc_in_db)
    return pc_in_db

def delete_pc_db(db: Session, physical_number:int) -> bool:
    """ DELETE """
    pc_in_db = __read_pc_by_field(db=db, field_name="physical_number", value=physical_number)
    if pc_in_db:
        return False
    db.delete(pc_in_db)
    db.commit()
    return True