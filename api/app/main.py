from fastapi import FastAPI
from app.routers import groups, tasks, users, token
from app.errors import init_error_handlers


app = FastAPI()

app.include_router(groups.router)
app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(token.router)

init_error_handlers(app)
