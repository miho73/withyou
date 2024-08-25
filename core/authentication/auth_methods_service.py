from enum import Enum
from typing import Union

from requests import Session

from models.auth_methods import AuthMethods
from models.user import User
from sql.repository import google_method_repository


class OAuthMethods(Enum):
    GOOGLE = "google"
    KAKAO = "kakao"
    PASSWORD = "password"

def find_user(unique_id: str, method: OAuthMethods, db: Session) -> Union[User, None]:
    if method == OAuthMethods.GOOGLE:
        auth_methods = find_google_user(unique_id, db)
    else:
        return None

    if auth_methods is None:
        return None

    return auth_methods.user


def find_google_user(google_id: str, db: Session) -> Union[AuthMethods, None]:
    method = google_method_repository.select_by_id(db, google_id)

    if method is None:
        return None

    return method.auth_methods