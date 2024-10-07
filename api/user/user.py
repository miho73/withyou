import logging

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
from schemas.user import UserSchema, JwtUser
from sql.database import create_connection
from sql.repository import user_repository, password_method_repository

router = APIRouter(
    prefix="/api/user",
    tags=["user"]
)

log = logging.getLogger(__name__)

def get_active_user(db: Session = Depends(create_connection), authorization: str = Depends(oauth_schema)) -> JwtUser:
    log.debug("Getting user information upon JWT. jwt=\"{}\"".format(authorization))
    token = authorize_jwt(authorization)

    sub = token.get("sub")

    user = user_repository.get_user_by_uid(db, sub)
    if user is None:
        log.debug("User specified by JWT was not found. user_uid=\"{}\"".format(sub))
        raise HTTPException(status_code=400, detail="User not found")

    log.debug("User information retrieved. user=\"{}\", ".format(user.role))
    jwt_user = JwtUser(
        uid=user.uid,
        uname=user.uname,
        email=user.email,
        email_verified=user.email_verified,
        role=user.role
    )
    return jwt_user


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
def get_user(user: JwtUser = Security(get_active_user)):
    log.debug("Responding user information. user_uid=\"{}\"".format(user.uid))
    return JSONResponse(
        content={
            "code": 200,
            "state": "OK",
            "user": {
                "uid": user.uid,
                "uname": user.uname,
                "email": user.email,
                "email_verified": user.email_verified,
                "role": str(user.role)
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
    log.debug("Adding new user. user_id=\"{}\", email=\"{}\"".format(user_body.id, user_body.email))
    recaptcha = verify_recaptcha(user_body.recaptcha, request.client.host, "signup")
    if not recaptcha:
        log.debug("Recaptcha verification failed and signup was canceled. user_id=\"{}\"".format(user_body.id))
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

    user_service.add_user(
        user,
        OAuthMethods.PASSWORD,
        {
            'user_id': user_body.id,
            'password': user_body.password
        },
        db
    )
    db.commit()

    log.debug("User added successfully. user_id=\"{}\"".format(user_body.id))
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
def check_user_id(request: Request, db: Session = Depends(create_connection)):
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
