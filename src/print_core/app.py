from fastapi import FastAPI

from print_core.api import router
from print_core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Print Core API")
    app.state.settings = settings
    app.include_router(router)

    return app
