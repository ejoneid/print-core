# print-core

FastAPI service that controls a Bambu Lab 3D printer. It syncs `.3mf` files from S3 to the printer's cache via FTP and exposes endpoints for printer status and file management.

## Endpoints

- `GET /status` - Health check
- `GET /printer/status` - Printer state, bed temperature, and Wi-Fi signal
- `GET /files` - List files on the printer
- `GET /files/cache` - List cached files on the printer
- `POST /files/cache` - Download files from S3 and upload to printer cache
- `POST /print` - Start a print (WIP)

## Setup

Requires Python 3.14+ and [uv](https://github.com/astral-sh/uv). A Nix flake is provided for dev tooling.

```bash
uv sync
cp .env.example .env  # fill in printer and S3 credentials
python wsgi.py         # runs on port 18000
```

## SSH Tunnel

A reverse SSH tunnel exposes the local API (port 18000) on the remote Docker host (port 19001) so containers can reach it. See [tunnel.md](tunnel.md) for server configuration details.
