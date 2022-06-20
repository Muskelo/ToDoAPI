from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from passlib.hash import pbkdf2_sha256
from app.models import TaskModel, GroupModel, UserModel


class BaseCRUD:
    def __init__(self, Model) -> None:
        self.Model = Model

    def create(self, db: Session, data: dict):
        item = self.Model(**data)
        db.add(item)
        db.commit()
        return item

    def get_list(self, db: Session):
        items_list = db.query(self.Model).all()
        return items_list

    def get(self, db: Session, filter_by: dict[str, Any] | None = None):
        query = db.query(self.Model)

        if filter_by:
            query = query.filter_by(**filter_by)

        return query.one()

    def get_by_id(self, db: Session, id: int):
        return self.get(db, {"id": id})

    def update(self, db: Session, id: int, data: dict):
        item = self.get_by_id(db, id)

        for attr, value in data.items():
            setattr(item, attr, value)

        db.add(item)
        db.commit()
        return item

    def delete(self, db: Session, id: int):
        item = self.get_by_id(db, id)
        db.delete(item)
        db.commit()
        return item


class UserCrud(BaseCRUD):
    def create(self, db: Session, data: dict) -> UserModel:

        # change password on password_hash
        password = data.pop('password')
        password_hash = pbkdf2_sha256.hash(password)
        data['password_hash'] = password_hash

        user = super().create(db, data)
        return user

    def authenticate_user(self, db: Session, login: str, password: str) -> UserModel | bool:
        try:
            user = self.get(db, {"login": login})
        except NoResultFound:
            return False

        if not pbkdf2_sha256.verify(password, user.password_hash):
            return False

        return user


task_crud = BaseCRUD(TaskModel)
group_crud = BaseCRUD(GroupModel)
user_crud = UserCrud(UserModel)
