from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class GroupModel(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    # relationships
    tasks = relationship("TaskModel", cascade="delete, all",
                         back_populates="group")


class TaskModel(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    completed = Column(Boolean, default=False)

    # foreign keys
    group_id = Column(Integer, ForeignKey("group.id"))

    # relationships
    group = relationship("GroupModel", back_populates="tasks")
