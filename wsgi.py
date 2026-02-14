import uvicorn

from print_core import create_app

app = create_app()

if __name__ == "__main__":
    # For local dev: `python wsgi.py`
    uvicorn.run("wsgi:app", host="0.0.0.0", port=18000, reload=True)
