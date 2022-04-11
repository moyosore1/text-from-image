import pathlib

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = pathlib.Path(__file__).parent


app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR/"templates"))


@app.get("/", response_class=HTMLResponse)
def index(request: Request):

    return {"key": "value"}