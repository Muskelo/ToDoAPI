from fastapi import Cookie, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth import decode_token
from app.crud import user_crud
from app.database import SessionLocal
from app.errors import InvalidCreadentialsError
from app.schemas.auth import Login


oauth2_scheme = OAuth2PasswordBearer("/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    payload = decode_token(token)
    user_id = payload.get("user_id")
    if user_id is None:
        raise InvalidCreadentialsError(
            detail="Missing user id in access token")
    return user_id


def get_current_user(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user = user_crud.get_or_none(db, {"id": current_user_id})
    if user is None:
        raise InvalidCreadentialsError(detail="Not such user")
    return user


def get_user_by_refresh_token(
    refresh_token: str = Cookie(),
    db: Session = Depends(get_db)
):
    decode_token(refresh_token)
    user = user_crud.get_or_none(db, {"refresh_token": refresh_token})
    if not user is None:
        raise InvalidCreadentialsError(detail="Invalid refresh token")
    return user


def get_authenticated_user(request_data: Login, db: Session = Depends(get_db)):
    user = user_crud.authenticate_user(
        db, request_data.login, request_data.password)
    if user is None:
        raise InvalidCreadentialsError(detail="Invalid login or password")
    return user
