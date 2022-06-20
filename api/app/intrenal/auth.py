import os
from typing import Callable
from datetime import datetime, timedelta

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from pydantic import BaseModel


# CONSTANS
SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = os.environ['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'])


# DEPENDENCIES
oauth2_scheme = OAuth2PasswordBearer('token')


# CHEMAS
class Login(BaseModel):
    login: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# EXCEPTIONS
# class MissingCallbackError(Exception):
#     pass


# UTILS
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# MAIN
class Auth:
    def __init__(self, get_db: Callable, authenticate_user: Callable) -> None:

        # get_db, authenticate_user callbacks
        self.get_db_callback = get_db
        self.authenticate_user_callback = authenticate_user

    def create_router(self) -> APIRouter:
        router = APIRouter(prefix="/token", tags=['auth'])

        @router.post('/', response_model=Token)
        def login_for_access_token(request_data: Login, db: Session = Depends(self.get_db_callback)):
            user = self.authenticate_user_callback(
                db=db,
                login=request_data.login,
                password=request_data.password)

            if not user:
                raise HTTPException(
                    status_code=401,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            access_token = create_access_token({'sub': user.id})
            return {"access_token": access_token, "token_type": "bearer"}

        return router


def init_auth(app: FastAPI, get_db: Callable, authenticate_user: Callable):
    auth = Auth(get_db=get_db, authenticate_user=authenticate_user)
    auth_router = auth.create_router()
    app.include_router(auth_router)
