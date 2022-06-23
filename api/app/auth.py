import os
from datetime import datetime, timedelta
from jose import jwt, JWTError

from app.errors import InvalidCreadentialsError

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINS = int(os.environ["ACCESS_TOKEN_EXPIRE_MINS"])
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ["REFRESH_TOKEN_EXPIRE_DAYS"])


def decode_token(token: str):
    try:
        return jwt.decode(token,
                          SECRET_KEY,
                          algorithms=ALGORITHM)

    except JWTError:
        raise InvalidCreadentialsError(
            detail="Could not validate credentials",
        )


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINS)
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM)
