from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app.crud import task_crud
from app.dependencies import get_db
from app.schemas.tasks import CreateTask, Task, UpdateTask


router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.post('/', response_model=Task)
def create_task_endpoint(request_body: CreateTask, db: Session = Depends(get_db)):
    task = task_crud.create(db, request_body.dict())
    return task


@router.get('/', response_model=list[Task])
def get_tasks_list_endpoint(db: Session = Depends(get_db)):
    tasks_list = task_crud.get_list(db)
    return tasks_list


@router.get('/{task_id}', response_model=Task)
def get_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    task = task_crud.get(db, task_id)
    return task


@router.patch('/{task_id}', response_model=Task)
def update_task_enpoint(task_id: int, request_body: UpdateTask, db: Session = Depends(get_db)):
    task = task_crud.update(db, task_id, request_body.dict(exclude_none=True))
    return task


@router.delete('/{task_id}', response_model=Task)
def delete_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    task = task_crud.delete(db, task_id)
    return task
