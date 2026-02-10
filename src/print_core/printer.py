from bambulabs_api import Printer

from print_core.config import get_settings

settings = get_settings()
printer = Printer(
    settings.printer_ip, settings.printer_serial, settings.printer_access_code
)
