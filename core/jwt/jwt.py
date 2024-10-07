from datetime import datetime, timedelta

import jwt
from jwt import InvalidTokenError

from config import config
from models.user import Role

DB_ROLE_CODE_TO_ROLE = {
    'USER': ['with:user'],
    'ADMIN': ['with:user', 'with:admin']
}

def create_token(user_id: int, role: Role) -> str:
    payload = {
        'aud': DB_ROLE_CODE_TO_ROLE[role],
        'sub': user_id,
        'exp': datetime.utcnow() + timedelta(weeks=5),
        'iat': datetime.utcnow(),
        'iss': 'with',
    }

    return jwt.encode(
        payload = payload,
        key = config['security']['jwt_secret'],
        algorithm ='HS256',
    )

def validate_token(token: str) -> bool:
    try:
        jwt.decode(
            jwt = token,
            key = config['security']['jwt_secret'],
            algorithms = ['HS256'],
            verify_signature=True,
            issuer='with',
            require=['aud', 'exp', 'iat', 'iss'],
            audience=['with:user', 'with:admin']
        )
    except InvalidTokenError as e:
        return False

    return True

def decode(token: str) -> dict:
    return jwt.decode(
        jwt = token,
        key = config['security']['jwt_secret'],
        algorithms = ['HS256'],
        verify_signature=True,
        issuer='with',
        require=['aud', 'exp', 'iat', 'iss'],
        audience=['with:user', 'with:admin'],
    )

def validate_authentication(token: str) -> bool:
    try:
        jwt.decode(
            jwt = token,
            key = config['security']['jwt_secret'],
            algorithms = ['HS256'],
            verify_signature=True,
            issuer='with',
            require=['aud', 'exp', 'iat', 'iss'],
            audience=['with:user', 'with:admin'],
        )
    except InvalidTokenError:
        return False

    return True