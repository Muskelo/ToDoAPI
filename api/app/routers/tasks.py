from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app.crud import task_crud, group_crud
from app.dependencies import get_current_user_id, get_db
from app.schemas.tasks import CreateTask, Task, UpdateTask


router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.post('/', response_model=Task)
def create_task_endpoint(request_body: CreateTask, owner_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    data = request_body.dict()
    data["owner_id"] = owner_id
    return task_crud.create(db, data)


@router.get('/', response_model=list[Task])
def get_tasks_list_endpoint(owner_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return task_crud.get_list(db, {"owner_id": owner_id})


@router.get('/{task_id}', response_model=Task)
def get_task_endpoint(task_id: int, owner_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return task_crud.get(db, {"id": task_id, "owner_id": owner_id})


@router.patch('/{task_id}', response_model=Task)
def update_task_endpoint(request_body: UpdateTask, task_id: int, owner_id: int = Depends(get_current_user_id),  db: Session = Depends(get_db)):
    task = task_crud.get(db, {"id": task_id, "owner_id": owner_id})
    return task_crud.update(db, request_body.dict(exclude_none=True), task)


@router.patch('/{task_id}/move/{group_id}', response_model=Task)
def move_task_endpoint(group_id: int,  task_id: int, owner_id: int = Depends(get_current_user_id),  db: Session = Depends(get_db)):
    # to validate owner of group
    group = group_crud.get(db, {"id": group_id, "owner_id": owner_id})
    task = task_crud.get(db, {"id": task_id, "owner_id": owner_id})
    return task_crud.update(db, {"group_id": group.id}, task)


@router.delete('/{task_id}', response_model=Task)
def delete_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    task = task_crud.delete(db, task_id)
    return task
