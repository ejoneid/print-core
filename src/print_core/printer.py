import logging

from bambulabs_api import Printer

from print_core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

missing = [
    name
    for name, value in {
        "printer_ip": settings.printer_ip,
        "printer_access_code": settings.printer_access_code,
        "printer_serial": settings.printer_serial,
    }.items()
    if not value
]
if missing:
    raise ValueError(
        "Missing printer settings: "
        + ", ".join(missing)
        + ". Check your environment configuration."
    )


def connect_printer() -> Printer:
    printer = Printer(
        settings.printer_ip,
        settings.printer_access_code,
        settings.printer_serial,
    )
    try:
        printer.connect()
    except Exception as exc:
        logger.warning(
            "Printer connection failed.",
            exc_info=exc,
        )
    return printer


def disconnect_printer(printer: Printer) -> None:
    try:
        printer.disconnect()
    except Exception as exc:
        logger.warning(
            "Printer disconnect failed; connection may already be closed.",
            exc_info=exc,
        )
