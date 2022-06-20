from pydantic import BaseModel


class BaseUser(BaseModel):
    login: str


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True


class CreateUser(BaseUser):
    password: str
