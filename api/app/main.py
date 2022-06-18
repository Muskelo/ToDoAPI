from fastapi import FastAPI
from .routers import groups, tasks
from app.errors import init_error_handlers


app = FastAPI()

app.include_router(groups.router)
app.include_router(tasks.router)

init_error_handlers(app)
