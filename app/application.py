from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .container import Container
from . import endpoints


def create_app() -> FastAPI:
    container = Container()

    db = container.db()
    db.create_database()

    app = FastAPI()
    app.container = container
    origins = [
        "http://localhost",
        "http://localhost:3000",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["PUT", "GET"],
        allow_headers=["*"],
    )
    app.include_router(endpoints.router)
    return app


app = create_app()
