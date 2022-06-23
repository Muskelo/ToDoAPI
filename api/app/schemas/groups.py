from pydantic import BaseModel


class _Task(BaseModel):
    id: int
    name: str
    completed: bool

    class Config:
        orm_mode = True


class Group(BaseModel):
    id: int
    name: str
    tasks: list[_Task]

    class Config:
        orm_mode = True


class CreateGroup(BaseModel):
    name: str


class UpdateGroup(BaseModel):
    name: str | None
