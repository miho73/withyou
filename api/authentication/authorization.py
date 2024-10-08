import logging

from fastapi import APIRouter, HTTPException
from fastapi.params import Security
from starlette.responses import JSONResponse

from api.authentication.google_signin import router
from core.authentication.authorization import oauth_schema, authorize_jwt

route = APIRouter(
    prefix="/api/auth",
    tags=["authentication"],
)

log = logging.getLogger(__name__)

@router.post(
    path = "/authorization",
    summary = "Authorize user with JWT token",
    description = "Authorize user with JWT token. This endpoint will check if the JWT token is valid and return if the user is authorized or not.",
    responses = {
        200: {
            "description": "JWT is ok and user is authorized",
            "content": {
                "application/json": {
                    "example": {
                        "code": 200,
                        "state": "OK",
                        "authorized": True
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
                            "authorized": {
                                "type": "boolean"
                            }
                        }
                    }
                }
            }
        },
        401: {
            "description": "JWT is invalid or unauthorized",
            "content": {
                "application/json": {
                    "example": {
                        "code": 401,
                        "state": "Unauthorized",
                        "message": "You are not authorized to access this resource"
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
def authorize_user(auth: str = Security(oauth_schema)):
    log.debug("Authorizing user with JWT token. jwt: {token}".format(token = auth))
    authorize_jwt(auth)

    return JSONResponse(
        status_code=200,
        content={
            "code": 200,
            "state": "OK",
            "authorized": True
        }
    )
