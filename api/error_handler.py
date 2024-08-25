from fastapi import HTTPException
from fastapi.routing import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

HTTP_CODE_TO_STATE = {
    200: "OK",
    201: "Created",
    202: "Accepted",
    204: "No Content",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    413: "Payload Too Large",
    415: "Unsupported Media Type",
    429: "Too Many Requests",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout"
}

def http_exception_handler(request: Request, exc: HTTPException):
    response = JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "state": HTTP_CODE_TO_STATE[exc.status_code],
            "message": exc.detail
        }
    )

    if exc.status_code == 401:
        response.headers["WWW-Authenticate"] = "Bearer"

    return response

def http_unauthorized_handler(request: Request, exc):
    return JSONResponse(
        status_code=401,
        headers={"WWW-Authenticate": "Bearer"},
        content={
            "code": 401,
            "state": "Unauthorized",
            "message": "You are not authorized to access this resource"
        }
    )

def http_internal_server_error_handler(request: Request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "state": "Internal Server Error",
            "message": "Server currently unable to handle this request"
        }
    )

def http_not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "code": 404,
            "state": "Not found",
            "message": "The requested resource could not be found"
        }
    )

def add_error_handler(app):
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(HTTP_500_INTERNAL_SERVER_ERROR, http_internal_server_error_handler)
    app.add_exception_handler(HTTP_404_NOT_FOUND, http_not_found_handler)
    return app