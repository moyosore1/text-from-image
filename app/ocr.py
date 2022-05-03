import pathlib


import pytesseract
from PIL import Image

BASE_DIR = pathlib.Path(__file__).parent
IMG_DIR = BASE_DIR / "images"
image_path = IMG_DIR / "jinja.png"

image = Image.open(image_path)

prediction = pytesseract.image_to_string(image)
