import os
import tempfile

from fastapi import APIRouter, HTTPException, Request, Response

from print_core.dependencies import PrinterDep
from print_core.s3_client import s3_client
from print_core.utils import parse_unixls_listings

router = APIRouter()


@router.get("/status")
def health_check() -> dict:
    return {"status": "ok"}


@router.get("/printer/status")
def printer_status(printer: PrinterDep) -> dict:
    status = printer.get_state()
    temp = printer.get_bed_temperature()
    wifi = printer.wifi_signal()
    return {"status": status, "temperature": temp, "wifi": wifi}


@router.get("/files")
def get_files(printer: PrinterDep) -> dict:
    printer_ls = printer.ftp_client.list_directory()[1]
    files = parse_unixls_listings(printer_ls)
    return {"files": [file.name for file in files]}


@router.get("/files/cache")
def get_cached_files(printer: PrinterDep) -> dict:
    printer_cache_ls = printer.ftp_client.list_cache_dir()[1]
    cache_files = parse_unixls_listings(printer_cache_ls)
    return {"files": [file.name for file in cache_files]}


@router.post("/files/cache")
async def upload_files(request: Request, printer: PrinterDep):
    files_to_upload = (await request.json())["files"]
    if not isinstance(files_to_upload, list) or not all(
        isinstance(file, str) for file in files_to_upload
    ):
        raise HTTPException(status_code=400, detail="files must be a list of strings")

    printer_cache_ls = printer.ftp_client.list_cache_dir()[1]
    cache_files = parse_unixls_listings(printer_cache_ls)
    cache_file_names = {file.name for file in cache_files}
    missing_files = [file for file in files_to_upload if file not in cache_file_names]
    if len(missing_files) == 0:
        return Response(status_code=204)

    for file in missing_files:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_path = tmp_file.name
        try:
            s3_client.download_file(
                Bucket=request.app.state.settings.s3_bucket_name,
                Key=file,
                Filename=tmp_path,
            )
            try:
                printer.ftp_client.upload_file(file, f"/cache/{file}")
            except TypeError as inner_exc:
                raise HTTPException(
                    status_code=500,
                    detail="Unable to upload file to printer FTP client",
                ) from inner_exc
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    return {"uploaded": missing_files}


@router.post("/print")
def start_print(request: Request):
    pass
