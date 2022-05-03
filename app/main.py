import pathlib
from functools import lru_cache
import io
import uuid


from fastapi import (FastAPI,
                     Request,
                     Depends,
                     File,
                     Header,
                     UploadFile,
                     HTTPException,
                     )
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings
from PIL import Image
import pytesseract



class Settings(BaseSettings):
    debug: bool = False
    echo_active: bool = False
    app_auth_token: str
    app_auth_token_prod: str = None
    skip_auth: bool = False

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()


BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"

settings = get_settings()
DEBUG = settings.debug


app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


def verify_auth(authorization=Header(None), settings: Settings = Depends(get_settings)):
    """
    Authorization: Bearer <token>
    {"authorization": "Bearer <token>"}
    """
    if settings.debug and settings.skip_auth:
        return
    if authorization is None:
        raise HTTPException(detail="Invalid endpoint", status_code=401)
    label, token = authorization.split()
    if token != settings.app_auth_token:
        raise HTTPException(detail="Invalid endpoint", status_code=401)


@app.post("/")
async def prediction_view(file: UploadFile = File(...), authorization=Header(None), settings: Settings = Depends(get_settings)):
    verify_auth(authorization, settings)
    file_bytes = io.BytesIO(await file.read())
    try:
        img = Image.open(file_bytes)
    except:
        raise HTTPException(detail="Invalid image", status_code=400)
    predictions_original = pytesseract.image_to_string(img)
    predictions = [x for x in predictions_original.split("\n")]
    return {"results": predictions, "original": predictions_original}


@app.post("/image-echo/", response_class=FileResponse)
async def image_echo_view(file: UploadFile = File(...), settings: Settings = Depends(get_settings)):
    if not settings.echo_active:
        raise HTTPException(detail="Invalid endpoint", status_code=400)
    UPLOAD_DIR.mkdir(exist_ok=True)
    file_bytes = io.BytesIO(await file.read())
    try:
        img = Image.open(file_bytes)
    except:
        raise HTTPException(detail="Invalid image", status_code=400)

    fname = pathlib.Path(file.filename)
    fext = fname.suffix  # e.g .txt

    dest = UPLOAD_DIR / f"{uuid.uuid1()}{fext}"
    img.save(dest)
    return dest
