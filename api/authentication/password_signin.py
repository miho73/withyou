import logging

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from core import password
from core.google.recaptcha import verify_recaptcha
from core.jwt import jwt
from schemas.request_models.auth_requests import PasswordSignInRequest
from schemas.user import UserSchema
from sql.database import create_connection

log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/auth",
    tags=["authentication"],
)

@router.post(
    path="/signin/password",
    summary="Signin with password",
    description="Signin with password. This endpoint will authenticate the user with the provided id and password. And return JWT token if the user is authenticated.",
    responses={
        200: {
            "description": "User is authenticated",
            "content": {
                "application/json": {
                    "example": {
                        "code": 200,
                        "state": "OK",
                        "token": "JWT_TOKEN"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "integer"
                            },
                            "state": {
                                "type": "string"
                            },
                            "token": {
                                "type": "string"
                            }
                        }
                    }
                }
            }
        },
        400: {
            "description": "User is not authenticated",
            "content": {
                "application/json": {
                    "example": {
                        "code": 400,
                        "state": "Bad Request",
                        "message": "REASON"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "integer"
                            },
                            "state": {
                                "type": "string"
                            },
                            "message": {
                                "type": "string"
                            }
                        }
                    }
                }
            }
        }
    }
)
def signin_password(user_body: PasswordSignInRequest, request: Request, db: Session = Depends(create_connection)):
    log.info("Signin with password. id=\"{}\"".format(user_body.id))
    recaptcha = verify_recaptcha(user_body.recaptcha, request.client.host, "signin_password")

    if not recaptcha:
        log.debug("Recaptcha verification failed and signin was canceled. user_id=\"{}\"".format(user_body.id))
        return JSONResponse(
            content={
                "code": 400,
                "state": "Bad Request",
                "message": "Recaptcha verification failed"
            },
            status_code=400
        )

    user: UserSchema = password.user_service.authenticate_user(user_body.id, user_body.password, db)
    jwt_token = jwt.create_token(user.uid, user.role)

    db.commit()
    return JSONResponse(
        content={
            "code": 200,
            "state": "OK",
            "result": "success",
            "token": jwt_token
        }
    )
