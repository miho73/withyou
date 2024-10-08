import logging
from datetime import datetime

from sqlalchemy.orm import Session

from core.authentication.auth_methods_service import OAuthMethods
from models import AuthMethods
from models.user import User
from sql.repository import auth_methods_repository, password_method_repository
from sql.repository import google_method_repository
from sql.repository import user_repository

log = logging.getLogger(__name__)

def add_user(user: User, auth_method: OAuthMethods, per_oauth_object:dict, db: Session) -> User:
    user_repository.add(db, user)
    log.debug("User was added to user table. user_uid=\"{}\"".format(user.uid))

    auth_methods = AuthMethods(
        uuid=user.uid,
        google=auth_method == OAuthMethods.GOOGLE,
        kakao=auth_method == OAuthMethods.KAKAO,
        password=auth_method == OAuthMethods.PASSWORD
    )

    auth_methods_repository.add(db, auth_methods)
    log.debug("Auth methods was added to auth_methods table. auth_auid=\"{}\", default_method=\"{default}\"".format(auth_methods.uid, default=str(auth_method)))

    if auth_method == OAuthMethods.GOOGLE:
        google_method_repository.add(db, auth_methods.uid, per_oauth_object['google_id'])
        log.debug("Google method was added to google_methods table. auth_auid=\"{}\", google_id=\"{}\"".format(auth_methods.uid, per_oauth_object['google_id']))
    elif auth_method == OAuthMethods.KAKAO:
        pass
    elif auth_method == OAuthMethods.PASSWORD:
        password_method_repository.add(db, auth_methods.uid, per_oauth_object['user_id'], per_oauth_object['password'])
        log.debug("Password method was added to password_methods table. auth_auid=\"{}\", id=\"{}\"".format(auth_methods.uid, per_oauth_object['user_id']))
    else:
        raise ValueError("Invalid auth method")

    return user


def get_last_login(db: Session, uid: int) -> datetime:
    user: User = user_repository.get_user_by_uid(db, uid)
    log.debug("User information queried. uid=\"{}\"".format(user.uid))

    return user.last_login
