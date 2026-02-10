from fastapi import APIRouter

from print_core.config import get_settings
from print_core.printer import printer

router = APIRouter()


@router.get("/status")
def health_check() -> dict:
    return {"status": "ok"}


@router.get("/printer-status")
def version_check() -> dict:
    # printer.connect()
    # status = printer.get_state()
    # printer.disconnect()
    return vars(get_settings())
