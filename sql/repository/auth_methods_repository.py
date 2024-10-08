from optparse import Option
from typing import Optional

from sqlalchemy.orm import Session

from models.auth_methods import AuthMethods


def get_by_userid(db: Session, user_id: int) -> Optional[AuthMethods]:
    return (
        db.query(AuthMethods)
            .filter(
                AuthMethods.uuid == user_id
            )
        .first()
    )

def add(db: Session, auth_methods: AuthMethods):
    db.add(auth_methods)
    db.flush()
