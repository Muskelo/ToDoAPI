from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from app.models import TaskModel, GroupModel


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

    def get(self, db: Session, id: int):
        # try:
        item = db.query(self.Model).filter(self.Model.id == id).one()
        # except NoResultFound:
        #     raise HTTPException(404, detail="Item not found")

        return item

    def update(self, db: Session, id: int, data: dict):
        item = self.get(db, id)

        for attr, value in data.items():
            setattr(item, attr, value)

        db.add(item)
        db.commit()
        return item

    def delete(self, db: Session, id: int):
        item = self.get(db, id)
        db.delete(item)
        db.commit()
        return item


task_crud = BaseCRUD(TaskModel)
group_crud = BaseCRUD(GroupModel)
