from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.users import CreateUser, UpdateMe, User
from app.crud import user_crud
from app.dependencies import get_db,  get_current_user

router = APIRouter(prefix="/users", tags=['users'])


@router.post('/', response_model=User)
def create_user_endpoint(request_data: CreateUser, db: Session = Depends(get_db)):
    return user_crud.create(db, request_data.dict())


@router.get("/", response_model=User)
def get_current_user_endpoint(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch('/', response_model=User)
def update_me_endpoint(
    request_data: UpdateMe,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return user_crud.update(db, request_data.dict(exclude_none=True), current_user)


@router.delete('/', response_model=User)
def delete_me_endpoint(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return user_crud.delete(db, current_user)
