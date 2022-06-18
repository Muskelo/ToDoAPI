from pydantic import BaseModel


class BaseGroup(BaseModel):
    name: str


class _Task(BaseGroup):
    id: int
    name: str
    completed: bool

    class Config:
        orm_mode = True


class Group(BaseGroup):
    id: int
    tasks: list[_Task]

    class Config:
        orm_mode = True


class CreateGroup(BaseGroup):
    pass


class UpdateGroup(BaseModel):
    name: str | None
