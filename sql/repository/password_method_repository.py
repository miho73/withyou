from typing import Optional

from sqlalchemy.orm import Session

from models.password_method import PasswordMethod


def exists_by_userid(db: Session, userid: str) -> bool:
    return (
        db.query(PasswordMethod)
        .filter(
            PasswordMethod.userid == userid
        )
        .first() is not None
    )

def add(db: Session, auid: int, userid: str, password: str):
    new_password_method = PasswordMethod(auid=auid, userid=userid, password=password)
    db.add(new_password_method)
    db.flush()

def get_by_userid(db: Session, userid: str) -> Optional[PasswordMethod]:
    return (
        db.query(PasswordMethod)
        .filter(
            PasswordMethod.userid == userid
        )
        .first()
    )

