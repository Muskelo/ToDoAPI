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

    def _get_query(self, db: Session, filter_by: dict | None = None):
        query = db.query(self.Model)

        if filter_by:
            query = query.filter_by(**filter_by)

        return query

    def get(self, db: Session, filter_by: dict | None = None):
        query = self._get_query(db, filter_by)
        return query.one()

    def get_or_none(self, db: Session, filter_by: dict | None = None):
        query = self._get_query(db, filter_by)
        return query.first()

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


class GroupCRUD(BaseCRUD):
    def add_task(self, db: Session, group, task):
        group.tasks.append(task)
        db.add(group)
        db.commit()
        return group


class UserCRUD(BaseCRUD):
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
            # delete refresh_token if change password
            data["refresh_token"] = None
        return super().update(db, data, item)

    def authenticate_user(self, db: Session, login: str, password: str):
        user = self.get_or_none(db, {"login": login})

        if user and pbkdf2_sha256.verify(password, user.password_hash):
            return user


task_crud = BaseCRUD(TaskModel)
group_crud = GroupCRUD(GroupModel)
user_crud = UserCRUD(UserModel)
