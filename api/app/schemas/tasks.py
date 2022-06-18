from pydantic import BaseModel


class BaseTask(BaseModel):
    name: str
    group_id: int


class CreateTask(BaseTask):
    pass


class Task(BaseTask):
    id: int
    completed: bool

    class Config:
        orm_mode = True


class UpdateTask(BaseTask):
    name: str | None
    completed: bool | None
    group_id: int | None

