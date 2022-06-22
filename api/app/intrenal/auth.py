from typing import Callable, Any
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from pydantic import BaseModel


# CHEMAS

class Login(BaseModel):
    login: str
    password: str


class Refresh(BaseModel):
    refresh_token: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


# EXCEPTIONS

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


class Auth():
    def __init__(self,
                 secret_key: str,
                 algorithm: str = "HS256",
                 access_expire: timedelta = timedelta(minutes=30),
                 refresh_expire: timedelta = timedelta(days=30),

                 token_url: str = '/token') -> None:

        self.oauth2_scheme = OAuth2PasswordBearer(token_url)

        self.SECRET_KEY = secret_key
        self.ALGORITHM = algorithm
        self.ACCESS_EXPIRE = access_expire
        self.REFRESH_EXPIRE = refresh_expire

    # utils

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + self.ACCESS_EXPIRE
        to_encode.update({"exp": expire})

        return jwt.encode(
            to_encode,
            self.SECRET_KEY,
            algorithm=self.ALGORITHM)

    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + self.REFRESH_EXPIRE
        to_encode.update({"exp": expire})

        return jwt.encode(
            to_encode,
            self.SECRET_KEY,
            algorithm=self.ALGORITHM)

    def decode_token(self, token: str):
        try:
            return jwt.decode(token,
                              self.SECRET_KEY,
                              algorithms=self.ALGORITHM)

        except JWTError:
            raise InvalidCreadentialsError(
                detail="Could not validate credentials",
            )

    # dependencies

    def create_current_user_dependency(self, get_db: Callable, get_user: Callable):

        def current_user(token: str = Depends(self.oauth2_scheme), db: Session = Depends(get_db)):
            payload = self.decode_token(token)
            user = get_user(db, payload)
            if not user:
                raise InvalidCreadentialsError(detail="Not such user")
            return user

        return current_user

    def create_role_required_dependency(self, get_roles: Callable):

        class RoleRequired():
            def __init__(self, roles_requiered: list[str]) -> None:
                self.roles_requiered = roles_requiered

            def __call__(self, roles=Depends(get_roles)):
                if not set(roles).intersection(set(self.roles_requiered)):
                    raise NotEnoughPermissionError

        return RoleRequired
