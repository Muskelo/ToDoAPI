from pydantic import BaseModel


class CreateTask(BaseModel):
    name: str


class Task(BaseModel):
    id: int
    name: str
    completed: bool
    group_id: int | None

    class Config:
        orm_mode = True


class UpdateTask(BaseModel):
    name: str | None
    completed: bool | None
