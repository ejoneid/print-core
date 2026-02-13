from contextlib import asynccontextmanager

from fastapi import FastAPI

from print_core.api import router
from print_core.config import get_settings
from print_core.printer import (
    connect_printer,
    disconnect_printer,
)
from print_core.tunnel import tunnel


@asynccontextmanager
async def lifespan(app: FastAPI):
    printer = connect_printer()
    tunnel.start()

    app.state.printer = printer

    yield

    tunnel.stop()
    disconnect_printer(printer)


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Print Core API", lifespan=lifespan)
    app.state.settings = settings
    app.include_router(router)

    return app
