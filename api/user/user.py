from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Security
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from api.authentication.authorization import oauth_schema
from core.authentication.authorization import authorize_jwt
from core.jwt import jwt
from schemas.user import UserSchema
from sql.database import create_connection
from sql.repository import user_repository

router = APIRouter(
    prefix="/api/user",
    tags=["user"]
)

def get_active_user(db: Session = Depends(create_connection), authorization: str = Depends(oauth_schema)) -> UserSchema:
    token = authorize_jwt(authorization)

    sub = token.get("sub")

    user = user_repository.get_user_by_uid(db, sub)
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")

    user_schema = UserSchema(
        uid=user.uid,
        uname=user.uname,
        email=user.email,
        email_verified=user.email_verified,
        role=user.role
    )
    return user_schema


@router.get(
    path="/get",
    summary="Get user",
    description="Get user information. This endpoint will return the user information based on the JWT token provided.",
    responses={
        200: {
            "description": "User information",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "integer",
                            },
                            "state": {
                                "type": "string",
                            },
                            "user": {
                                "type": "object",
                                "properties": {
                                    "uid": {
                                        "type": "string"
                                    },
                                    "uname": {
                                        "type": "string"
                                    },
                                    "email": {
                                        "type": "string"
                                    },
                                    "email_verified": {
                                        "type": "boolean"
                                    },
                                    "role": {
                                        "type": "string"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        401: {
            "description": "Invalid JWT token",
            "content": {
                "application/json": {
                    "example": {
                        "type": "object",
                        "properties": {
                            "code": 401,
                            "state": "Unauthorized",
                            "message": "You are not authorized to access this resource"
                        }
                    }
                }
            }
        }
    }
)
def get_user(user: UserSchema = Security(get_active_user)):
    return JSONResponse(
        content={
            "code": 200,
            "state": "OK",
            "user": {
                "uid": user.uid,
                "uname": user.uname,
                "email": user.email,
                "email_verified": user.email_verified,
                "role": user.role
            }
        }
    )
