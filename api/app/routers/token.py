from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.intrenal.auth import Token, InvalidCreadentialsError, Login, Refresh
from app.intrenal import auth_instance
from app.crud import user_crud
from app.dependencies import get_db

router = APIRouter(prefix='/token')


def create_tokens(db: Session, user):
    access_token = auth_instance.create_access_token(
        {"sub": f"auth|{user.login}"})
    refresh_token = auth_instance.create_refresh_token(
        {"sub": f"refresh|{user.login}"})
    user_crud.update(db, user.id, {"refresh_token": refresh_token})

    return access_token, refresh_token


@router.post('/', response_model=Token)
def login_for_access_token(request_data: Login, db: Session = Depends(get_db)):
    user = user_crud.authenticate_user(
        db, request_data.login, request_data.password)

    if user is None:
        raise InvalidCreadentialsError(detail="Invalid login or password")

    access_token, refresh_token = create_tokens(db, user)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post('/refresh', response_model=Token)
def refresh_token(request_data: Refresh, db: Session = Depends(get_db)):
    # check expire
    auth_instance.decode_token(request_data.refresh_token)

    user = user_crud.get_or_none(
        db, {"refresh_token": request_data.refresh_token})

    if not user:
        raise InvalidCreadentialsError(detail="Invalid refresh_token")

    access_token, refresh_token = create_tokens(db, user)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
