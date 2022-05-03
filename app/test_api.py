import shutil
import time
import io

from fastapi.testclient import TestClient
from PIL import Image, ImageChops

from app.main import UPLOAD_DIR, app, BASE_DIR

# like python requests
client = TestClient(app)


def test_echo_image():
    image_folder_path = BASE_DIR / "images"
    for path in image_folder_path.glob("*"):
        try:
            img = Image.open(path)
        except:
            img = None
        response = client.post("/image-echo/", files={"file": open(path, 'rb')})

        if img is None:
            assert response.status_code == 400
        else:
            assert response.status_code == 200
            r_stream = io.BytesIO(response.content)
            echo_img = Image.open(r_stream)
            difference = ImageChops.difference(echo_img, img).getbbox()
            assert difference is None

    time.sleep(3)
    shutil.rmtree(UPLOAD_DIR)


# def test_predict_image():
#     image_folder_path = BASE_DIR / "images"
#     for path in image_folder_path.glob("*"):
#         try:
#             img = Image.open(path)
#         except:
#             img = None
#         # i.e requests.get("/")
#         response = client.post(
#             "/", files={"file": open(path, 'rb')})
#
#         if img is None:
#             assert response.status_code == 400
#         else:
#             assert response.status_code == 200
#             data = response.json()
#             print(data)
#             assert len(data.keys()) == 2
#
#     time.sleep(3)
#     shutil.rmtree(UPLOAD_DIR)
