import logging
from datetime import datetime
from platform import uname
from typing import Optional

from sqlalchemy.orm import Session

from core.cryptography.brypt import hash_bcrypt, verify_bcrypt
from models import User
from schemas.user import UserSchema
from sql.repository import auth_methods_repository, password_method_repository

log = logging.getLogger(__name__)

class AuthError(Exception):
    def __init__(self, message: str):
        self.message = message

def authenticate_user(username: str, password: str, db: Session) -> UserSchema:
    password_method = password_method_repository.get_by_userid(db, username)
    if password_method is None:
        log.debug("User not found. username=\"{username}\"".format(username=username))
        raise AuthError("invalid-credentials")

    if not verify_bcrypt(password, password_method.password):
        log.debug("Password is incorrect. username=\"{username}\"".format(username=username))
        raise AuthError("invalid-credentials")

    user: User = password_method.auth_methods.user
    user.last_login = datetime.now()

    return UserSchema(
        uid=user.uid,
        uname=user.uname,
        email=user.email,
        email_verified=user.email_verified,
        role=user.role,
        sex=user.sex
    )
