from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class UserModel(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    login = Column(String(255), unique=True)
    password_hash = Column(String(255))
    refresh_token = Column(String(255))

    # relationships
    groups = relationship("GroupModel", cascade="delete, all",
                          back_populates="owner")
    tasks = relationship("TaskModel", cascade="delete, all",
                         back_populates="owner")


class GroupModel(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    # foreign keys
    owner_id = Column(Integer, ForeignKey("user.id"))
    # relationships
    owner = relationship("UserModel", back_populates="groups")
    tasks = relationship("TaskModel", cascade="delete, all",
                         back_populates="group")


class TaskModel(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    completed = Column(Boolean, default=False)

    # foreign keys
    owner_id = Column(Integer, ForeignKey("user.id"))
    group_id = Column(Integer, ForeignKey("group.id"))

    # relationships
    owner = relationship("UserModel", back_populates="tasks")
    group = relationship("GroupModel", back_populates="tasks")
