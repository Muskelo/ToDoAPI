from fastapi import Depends
from app.database import SessionLocal
from app.crud import user_crud
from app.intrenal import auth_instance


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


current_user = auth_instance.create_current_user_dependency(
    get_db, user_crud.get_user_from_payload
)


def get_roles(current_user=Depends(current_user)):
    return [current_user.role]


RoleRequired = auth_instance.create_role_required_dependency(get_roles)
