from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class UserModel(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    login = Column(String(255), unique=True)
    password_hash = Column(String(255))
    role = Column(String(255), default="user")
    refresh_token = Column(String(255))


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
