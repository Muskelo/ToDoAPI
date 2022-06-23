from pydantic import BaseModel


class BaseTask(BaseModel):
    name: str


class CreateTask(BaseTask):
    pass


class Task(BaseTask):
    id: int
    completed: bool
    group_id: int | None

    class Config:
        orm_mode = True


class UpdateTask(BaseTask):
    name: str | None
    completed: bool | None

