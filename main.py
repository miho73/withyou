import logging

import uvicorn
from fastapi import FastAPI

from api.error_handler import add_error_handler
from api.user import user

app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url="/api/redoc",
)

from api.authentication import google_signin, authorization, kakao_signin

log = logging.getLogger(__name__)

log.info("Starting server")

# #authentication
log.info("Adding authentication routers")
app.include_router(google_signin.router)
app.include_router(kakao_signin.router)
app.include_router(authorization.router)

# #user
log.info("Adding user router")
app.include_router(user.router)

add_error_handler(app)

log.info("Server ready to go")
