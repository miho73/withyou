import random
import string
from datetime import datetime

import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session

from config import config
from core import authentication, kakao
from core import jwt
from core import user_service
from core.authentication.auth_methods_service import OAuthMethods
from models.user import User, Role

def create_state(n: int) -> string:
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(n))

def start_authentication():
    state = create_state(16)

    authorization_url = config['auth']['kakao']['authorization_uri'].format(
        client_id=config['auth']['kakao']['client_id'],
        redirect_uri=config['auth']['kakao']['redirect_uri'],
        scope=config['auth']['kakao']['scope'],
        state=state
    )

    return authorization_url, state

def exchange_token(code: str):
    with httpx.Client() as cli:
        token_response = cli.post(
            url=config['auth']['kakao']['token_uri'],
            headers={
                'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
            },
            data={
                'grant_type': 'authorization_code',
                'client_id': config['auth']['kakao']['client_id'],
                'redirect_uri': config['auth']['kakao']['redirect_uri'],
                'code': code,
                'client_secret': config['auth']['kakao']['client_secret']
            },
        )

    if token_response.status_code is not 200:
        raise HTTPException(status_code=token_response.status_code, detail=token_response.text)

    response = token_response.json()
    if response.get('token_type') != 'bearer':
        raise HTTPException(status_code=500, detail="Kakao provider responded with invalid token type")

    if not response.get('access_token'):
        raise HTTPException(status_code=500, detail="Kakao provider responded without access token")

    return response.get('access_token')

def complete_oauth_flow(code: str, db: Session):
    # fetch user_service info
    access_token = exchange_token(code)

    # fetch user infomation
    kakao_user = kakao.user_service.get_user(access_token)

    # check if user exists
    user = authentication.auth_methods_service.find_user(kakao_user.id, OAuthMethods.GOOGLE, db)

    if user is None:
        user = User(
            uname = kakao_user.uname,
            email = kakao_user.email,
            email_verified = kakao_user.email_verified,
            role = Role.USER.value
        )
        user = user_service.add_user(user, OAuthMethods.GOOGLE, kakao_user.id, db)
    else:
        user.last_login = datetime.now()

    jwt_token = jwt.create_token(user.uid, user.role)
    return jwt_token
