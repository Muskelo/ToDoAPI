from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound, IntegrityError

error_messages = {
    "NoResultFound": "Item not found",
    "IntegrityError": "Possibly invalid foreign key or re-entry of unique data."
}


async def no_result_found_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=404, content={"detail": error_messages["NoResultFound"]})


async def integrity_error_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=409, content={"detail": error_messages["IntegrityError"]})


def init_error_handlers(app: FastAPI):
    app.add_exception_handler(NoResultFound, no_result_found_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)
