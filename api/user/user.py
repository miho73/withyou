from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends, Security
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from api.authentication.authorization import oauth_schema
from core.authentication.auth_methods_service import OAuthMethods
from core.authentication.authorization import authorize_jwt
from core.google.recaptcha import verify_recaptcha
from core.user_service import user_service
from models import User
from schemas.request_models.user_requests import AddUserRequest
from models.user import Role
from schemas.user import UserSchema
from sql.database import create_connection
from sql.repository import user_repository, password_method_repository

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

@router.post(
    path="/add",
    summary="Add user",
    description="Add a new user to the database with password authentication method",
    responses={
        200: {
            "description": "User added",
            "content": {
                "application/json": {
                    "example": {
                        "code": 200,
                        "state": "OK",
                    }
                }
            }
        }
    }
)
def add_user(user_body: AddUserRequest, request: Request, db: Session = Depends(create_connection)):
    recaptcha = verify_recaptcha(user_body.recaptcha, request.client.host, "signup")
    if not recaptcha:
        return JSONResponse(
            content={
                "code": 400,
                "state": "Bad Request",
                "message": "Recaptcha verification failed"
            },
            status_code=400
        )

    user = User(
        uname = user_body.name,
        email = user_body.email,
        email_verified = False,
        role = Role.ROLE_USER.value,
        sex = user_body.sex
    )

    user = user_service.add_user(
        user,
        OAuthMethods.PASSWORD,
        {
            'user_id': user_body.id,
            'password': user_body.password
        },
        db
    )
    db.commit()

    return JSONResponse(
        content={
            "code": 200,
            "state": "OK"
        }
    )

@router.get(
    path="/add/check-id",
    summary="Check if given user id is available",
    description="Check if given user id is available to use. This endpoint searches PasswordMethod table to check if the given user id is already used or not.",
    responses={
        200: {
            "description": "User id is available",
            "content": {
                "application/json": {
                    "example": {
                        "code": 200,
                        "state": "OK",
                    }
                }
            }
        },
    }
)
def checkUserId(request: Request, db: Session = Depends(create_connection)):
    id = request.query_params.get("id")
    if id is None:
        return JSONResponse(
            content={
                "code": 400,
                "state": "Bad Request",
                "message": "User id is not provided"
            },
            status_code=400
        )

    if password_method_repository.exists_by_userid(db, id):
        return JSONResponse(
            content={
                "code": 200,
                "state": "OK",
                "result": "taken"
            }
        )

    return JSONResponse(
        content={
            "code": 200,
            "state": "OK",
            "result": "available"
        }
    )
