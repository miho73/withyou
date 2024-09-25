from sqlalchemy.orm import Session

from core.authentication.auth_methods_service import OAuthMethods
from models import AuthMethods
from models.user import User
from sql.repository import auth_methods_repository, password_method_repository
from sql.repository import google_method_repository
from sql.repository import user_repository


def add_user(user: User, auth_method: OAuthMethods, per_oauth_object:dict, db: Session) -> User:
    user_repository.add(db, user)

    auth_methods = AuthMethods(
        uuid=user.uid,
        google=auth_method == OAuthMethods.GOOGLE,
        kakao=auth_method == OAuthMethods.KAKAO,
        password=auth_method == OAuthMethods.PASSWORD
    )

    auth_methods_repository.add(db, auth_methods)

    if auth_method == OAuthMethods.GOOGLE:
        google_method_repository.add(db, auth_methods.uid, per_oauth_object['google_id'])
    elif auth_method == OAuthMethods.KAKAO:
        pass
    elif auth_method == OAuthMethods.PASSWORD:
        password_method_repository.add(db, auth_methods.uid, per_oauth_object['user_id'], per_oauth_object['password'])
    else:
        raise ValueError("Invalid auth method")

    return user
