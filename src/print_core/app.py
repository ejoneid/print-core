from contextlib import asynccontextmanager

from fastapi import FastAPI

from print_core.api import router
from print_core.config import get_settings
from print_core.printer import (
    connect_printer,
    disconnect_printer,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    printer = connect_printer()

    app.state.printer = printer

    yield

    disconnect_printer(printer)


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Print Core API", lifespan=lifespan)
    app.state.settings = settings
    app.include_router(router)

    return app
