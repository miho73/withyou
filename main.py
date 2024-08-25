from fastapi import FastAPI

from api.error_handler import add_error_handler
from api.user import user

app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url="/api/redoc",
)

from api.authentication import google_signin, authorization, kakao_signin

# #authentication
app.include_router(google_signin.router)
app.include_router(kakao_signin.router)
app.include_router(authorization.router)

# #user
app.include_router(user.router)

add_error_handler(app)
