from pydantic import BaseModel


class BaseUser(BaseModel):
    login: str


class User(BaseUser):
    id: int
    role: str

    class Config:
        orm_mode = True


class CreateUser(BaseUser):
    password: str


class UpdateMe(BaseModel):
    login: str | None
    password: str | None
