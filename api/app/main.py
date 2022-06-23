from fastapi import FastAPI
from app.routers import groups, tasks, users, tokens
from app.errors import init_error_handlers


def create_app():
    app = FastAPI()

    app.include_router(groups.router)
    app.include_router(tasks.router)
    app.include_router(users.router)
    app.include_router(tokens.router)

    init_error_handlers(app)

    return app


app = create_app()
