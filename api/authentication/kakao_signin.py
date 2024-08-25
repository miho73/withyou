from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from config import config
from core.cryptography import aes256
from core.kakao.oauth import start_authentication, complete_oauth_flow
from sql.database import create_connection

router = APIRouter(
    prefix="/api/auth",
    tags=["authentication"],
)

@router.get(
    path="/signin/kakao",
    status_code=302,
    summary="Redirect frontend to Kakao Signin",
    description="Generate OAuth2 URL and redirect frontend to Kakao Signin page. This endpoint will set a cookie with state value to prevent CSRF attack as well.",
    responses={
        302: {
            "description": "Redirect to Kakao Signin",
            "headers": {
                "Location": {
                    "description": "Redirect URL",
                    "schema": {
                        "type": "string"
                    }
                }
            }
        }
    }
)
def start_signin_kakao():
    auth_url, state = start_authentication()

    e_state = aes256.encrypt(state)

    response = RedirectResponse(auth_url, 302)
    response.set_cookie(
        key="with-state",
        value=e_state,
        httponly=True,
        secure=config['env'] == "production",
        samesite="strict",
        path="/"
    )

    return response

@router.get(
    path="/callback/kakao",
    status_code=302,
    summary="Handle redirect from Kakao OAuth2",
    description="Handle redirect from Kakao OAuth2. This endpoint will check state and code from Kakao OAuth2 response. If state and code is valid, it will complete the OAuth2 flow and generate JWT token for the user. And pass the JWT token to frontend.",
    responses={
        302: {
            "description": "Redirect to frontend with JWT token",
            "headers": {
                "Location": {
                    "description": "Redirect URL",
                    "schema": {
                        "type": "string"
                    }
                }
            }
        }
    }
)
def callback_signin_kakao(request: Request, db: Session = Depends(create_connection)):
    if request.query_params.get("error"):
        return RedirectResponse("/auth/signin?error=kakao_error", 302)

    # check state
    e_cookie_state = request.cookies.get("with-state")
    response_state = request.query_params.get("state")
    if e_cookie_state is None or response_state is None:
        return RedirectResponse("/auth/signin?error=state_unset", 302)
    cookie_state = aes256.decrypt(e_cookie_state)
    if cookie_state is None or cookie_state != response_state:
        return RedirectResponse("/auth/signin?error=state_mismatch", 302)

    # check code
    code = request.query_params.get("code")
    if code is None:
        return RedirectResponse("/auth/signin?error=code_unset", 302)

    jwt = complete_oauth_flow(code, db)
    response = RedirectResponse("/auth/signin/complete?jwt={jwt}".format(jwt=jwt), 302)
    response.delete_cookie('with-state')

    return response
