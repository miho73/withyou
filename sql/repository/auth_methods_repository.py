from sqlalchemy.orm import Session

from models.auth_methods import AuthMethods


def get_by_userid(db: Session, user_id: int):
    return (
        db.query(AuthMethods)
            .filter(
                AuthMethods.uuid == user_id
            )
        .first()
    )

def add(db: Session, auth_methods: AuthMethods):
    db.add(auth_methods)
