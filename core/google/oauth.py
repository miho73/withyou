import logging

from google_auth_oauthlib.flow import Flow
from sqlalchemy.orm import Session

from config import config
from core import authentication
from core import google
from core import jwt
from core import user_service
from core.authentication.auth_methods_service import OAuthMethods
from models.user import User, Role

flow = Flow.from_client_secrets_file(
    client_secrets_file=config['auth']['google']['client_secret_file'],
    scopes=[
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
        'openid'
    ]
)
flow.redirect_uri = config['auth']['google']['redirect_uri']

def start_authentication():
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    return authorization_url, state

def complete_oauth_flow(code: str, db: Session):
    # fetch user_service info
    flow.fetch_token(code=code)
    credentials = flow.credentials
    google_user = google.user_service.get_user(credentials)

    # check if user exists
    user = authentication.auth_methods_service.find_user(google_user.id, OAuthMethods.GOOGLE, db)

    if user is None:
        user = User(
            uname = google_user.uname,
            email = google_user.email,
            email_verified = google_user.email_verified,
            role = Role.ROLE_USER.value
        )
        user = user_service.add_user(user, OAuthMethods.GOOGLE, {'google_id': google_user.id}, db)

    jwt_token = jwt.create_token(user.uid, user.role)
    return jwt_token
