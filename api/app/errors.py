from typing import Any
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound, IntegrityError

error_messages = {
    "NoResultFound": "Item not found",
    "IntegrityError": "Possibly invalid foreign key or re-entry of unique data."
}


class InvalidCreadentialsError(HTTPException):
    def __init__(self,
                 status_code: int = 401,
                 detail: Any = "Invalid credentials",
                 headers: dict[str, Any] | None = None) -> None:

        if not headers:
            headers = {}

        headers["WWW-Authenticate"] = "Bearer"
        super().__init__(status_code, detail, headers)


class NotEnoughPermissionError(HTTPException):
    def __init__(self,
                 status_code: int = 403,
                 detail: Any = "You don't have permission",
                 headers: dict[str, Any] | None = None) -> None:

        if not headers:
            headers = {}

        headers["WWW-Authenticate"] = "Bearer"
        super().__init__(status_code, detail, headers)


async def no_result_found_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=404, content={"detail": error_messages["NoResultFound"]})


async def integrity_error_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=409, content={"detail": error_messages["IntegrityError"]})


def init_error_handlers(app: FastAPI):
    app.add_exception_handler(NoResultFound, no_result_found_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)
