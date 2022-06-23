from sqlalchemy.orm import Session
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

    def get_list(self, db: Session, filter_by: dict | None = None):
        query = db.query(self.Model)

        if filter_by:
            query = query.filter_by(**filter_by)

        return query.all()

    def _get_base(self, db: Session, filter_by: dict | None = None):
        query = db.query(self.Model)

        if filter_by:
            query = query.filter_by(**filter_by)

        return query

    def get(self, db: Session, filter_by: dict | None = None):
        query = self._get_base(db, filter_by)
        return query.one()

    def get_or_none(self, *args, **kwargs):
        query = self._get_base(*args, **kwargs)
        return query.first()

    def get_by_id(self, db: Session, id: int):
        return self.get(db, {"id": id})

    def get_or_none_by_id(self, db: Session, id: int):
        return self.get_or_none(db, {"id": id})

    def update(self, db: Session, data: dict, item):
        for attr, value in data.items():
            setattr(item, attr, value)

        db.add(item)
        db.commit()
        return item

    def delete(self, db: Session, item):
        db.delete(item)
        db.commit()
        return item


class UserCrud(BaseCRUD):
    def _replace_password_on_hash(self, data: dict) -> dict:
        # change password on password_hash
        password = data.pop('password')
        password_hash = pbkdf2_sha256.hash(password)
        data['password_hash'] = password_hash
        return data

    def create(self, db: Session, data: dict):
        data = self._replace_password_on_hash(data)
        return super().create(db, data)

    def update(self, db: Session, data: dict, item):
        if "password" in data:
            data = self._replace_password_on_hash(data)
            data["refresh_token"] = None
        return super().update(db, data, item)

    def authenticate_user(self, db: Session, login: str, password: str):
        user = self.get_or_none(db, {"login": login})

        if not user:
            return

        if not pbkdf2_sha256.verify(password, user.password_hash):
            return

        return user


task_crud = BaseCRUD(TaskModel)
group_crud = BaseCRUD(GroupModel)
user_crud = UserCrud(UserModel)
