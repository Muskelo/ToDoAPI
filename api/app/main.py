from fastapi import FastAPI
from app.routers import groups, tasks, users
from app.intrenal.auth import init_auth
from app.crud import user_crud
from app.dependencies import get_db
from app.errors import init_error_handlers


app = FastAPI()

app.include_router(groups.router)
app.include_router(tasks.router)
app.include_router(users.router)

init_auth(app, get_db, user_crud.authenticate_user)

init_error_handlers(app)
