from datetime import datetime, timedelta

from jose import JWTError, jwt

from app.config import Config
from app.errors import InvalidCreadentialsError


def decode_token(token: str):
    try:
        return jwt.decode(token, Config.SECRET_KEY, algorithms=Config.ALGORITHM)
    except JWTError:
        raise InvalidCreadentialsError(detail="Could not validate credentials")


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=Config.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
