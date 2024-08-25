from fastapi import HTTPException
from fastapi.security import APIKeyHeader
from jwt import InvalidTokenError

from core.jwt import jwt


class APIKeyHeaderBearer(APIKeyHeader):
    def __init__(self):
        super().__init__(name="Authorization")

oauth_schema = APIKeyHeaderBearer()

def authorize_jwt(token: str):
    if token is None:
        raise HTTPException(status_code=400, detail="Authorization header is missing")

    if not token.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Authorization must be Bearer token")

    jwt_token = token[7:]
    if not jwt_token:
        raise HTTPException(status_code=400, detail="JWT token is missing")

    try:
        jwt_body = jwt.decode(jwt_token)
    except (InvalidTokenError, Exception):
        raise HTTPException(status_code=401, detail="JWT is invalid or unauthorized")

    if not jwt_body:
        raise HTTPException(status_code=401, detail="JWT is invalid or unauthorized")

    return jwt_body
