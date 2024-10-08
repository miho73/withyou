from optparse import Option
from typing import Optional

from sqlalchemy.orm import Session

from models.user import User


def get_user_by_uid(db: Session, uid: int) -> Optional[User]:
    return (
        db.query(User)
            .filter(
                User.uid == uid
            )
        .first()
    )

def add(db: Session, user: User):
    db.add(user)
    db.flush()
