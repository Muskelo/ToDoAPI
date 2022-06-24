from pydantic import BaseModel


class User(BaseModel):
    id: int
    login: str

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    login: str
    password: str


class UpdateUser(BaseModel):
    login: str | None
    password: str | None
