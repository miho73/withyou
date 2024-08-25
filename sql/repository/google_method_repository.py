from typing import Union

from sqlalchemy.orm import Session

from models.google_method import GoogleMethod


def select_by_id(db: Session, google_id: str) -> Union[GoogleMethod, None]:
    return (
        db.query(GoogleMethod)
        .filter(
            GoogleMethod.google_id == google_id
        )
        .first()
    )

def add(db: Session, auid: int, google_id: str):
    new_google_method = GoogleMethod(auid=auid, google_id=google_id)
    db.add(new_google_method)
