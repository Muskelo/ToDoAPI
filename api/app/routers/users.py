from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.users import CreateUser, User
from app.crud import user_crud
from app.dependencies import get_db

router = APIRouter(prefix="/users", tags=['users'])


@router.post('/', response_model=User)
def create_user_endpoint(request_data: CreateUser, db: Session = Depends(get_db)):
    user = user_crud.create(db, request_data.dict())
    return user


@router.get('/', response_model=list[User])
def get_users_list_endpoint(db: Session = Depends(get_db)):
    users_list = user_crud.get_list(db)
    return users_list
