from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.crud import user_crud
from app.dependencies import get_authenticated_user, get_db, get_user_by_refresh_token
from app.auth import create_access_token, create_refresh_token
from app.schemas.auth import Token

router = APIRouter(prefix='/token', tags=["auth"])


def create_tokens(user):
    access_token = create_access_token({
        "sub": f"auth|{user.login}",
        "user_id": user.id
    })
    refresh_token = create_refresh_token({
        "sub": f"refresh|{user.login}",
        "user_id": user.id
    })
    return access_token, refresh_token


def set_refresh_token(db: Session, refresh_token: str, resp: Response, user):
    user_crud.update(db, {"refresh_token": refresh_token}, item=user)
    resp.set_cookie("refresh_token", refresh_token, httponly=True)


@router.post('/', response_model=Token)
def login_for_access_token(
    resp: Response,
    user=Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):
    access_token, refresh_token = create_tokens(user)
    set_refresh_token(db, refresh_token, resp, user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/refresh', response_model=Token)
def refresh_token(
    resp: Response,
    user=Depends(get_user_by_refresh_token),
    db: Session = Depends(get_db)
):
    access_token, refresh_token = create_tokens(user)
    set_refresh_token(db, refresh_token, resp, user)
    return {"access_token": access_token, "token_type": "bearer"}
