from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user_id
from app.crud import group_crud, task_crud
from app.schemas.groups import CreateGroup, Group, UpdateGroup

router = APIRouter(prefix="/groups", tags=['groups'])


@router.post('/', response_model=Group)
def create_group_endpoint(request_body: CreateGroup, owner_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    data = request_body.dict()
    data["owner_id"] = owner_id
    return group_crud.create(db, data)


@router.get("/", response_model=list[Group])
def get_groups_list_endpoint(owner_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return group_crud.get_list(db, {"owner_id": owner_id})


@router.get("/{group_id}", response_model=Group)
def get_group_endpoint(group_id: int, owner_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return group_crud.get(db, {"id": group_id, "owner_id": owner_id})


@router.patch('/{group_id}', response_model=Group)
def update_group_endpoint(request_body: UpdateGroup, group_id: int, owner_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    group = group_crud.get(db, {"id": group_id, "owner_id": owner_id})
    return group_crud.update(
        db, request_body.dict(exclude_none=True), group)


@router.delete("/{group_id}", response_model=Group)
def delete_group_endpoint(group_id: int, owner_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    group = group_crud.get(db, {"id": group_id, "owner_id": owner_id})
    return group_crud.delete(db, group)
