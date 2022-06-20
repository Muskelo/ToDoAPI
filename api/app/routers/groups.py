from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.crud import group_crud
from app.schemas.groups import CreateGroup, Group, UpdateGroup

router = APIRouter(prefix="/groups", tags=['groups'])


@router.get("/", response_model=list[Group])
def get_groups_list_endpoint(db: Session = Depends(get_db)):
    groups_list = group_crud.get_list(db)
    return groups_list


@router.get('/{group_id}', response_model=Group)
def get_group_endpoint(group_id: int, db: Session = Depends(get_db)):
    group = group_crud.get_by_id(db, group_id)
    return group


@router.post('/', response_model=Group)
def create_group_endpoint(request_body: CreateGroup, db: Session = Depends(get_db)):
    group = group_crud.create(db, request_body.dict())
    return group


@router.patch('/{group_id}', response_model=Group)
def update_group_endpoint(group_id: int, request_body: UpdateGroup, db: Session = Depends(get_db)):
    group = group_crud.update(
        db, group_id, request_body.dict(exclude_none=True))
    return group


@router.delete("/{group_id}", response_model=Group)
def delete_group_endpoint(group_id: int, db: Session = Depends(get_db)):
    group = group_crud.delete(db, group_id)
    return group
