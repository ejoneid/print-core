from typing import Annotated

from bambulabs_api import Printer
from fastapi import Depends, Request


def get_printer(request: Request) -> Printer:
    return request.app.state.printer


PrinterDep = Annotated[Printer, Depends(get_printer)]
