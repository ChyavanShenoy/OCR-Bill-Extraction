import requests
import base64
import io
from PIL import Image
import uuid
import glob
import os


TEMP_FILE_DIR = "temp_files"


def download_file(url, file_name):
    r = requests.get(url, stream=True)
    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


def base64_to_image(base64_string):
    imgdata = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(imgdata))
    return image


def image_to_base64(image):
    with open("synth_image.jpg", "rb") as image_file:
        img_str = base64.b64encode(image_file.read())
    return img_str


def write_image_to_file(image):
    filename = TEMP_FILE_DIR + "/" + str(uuid.uuid4()) + ".jpg"
    image.save(filename)
    return filename


def delete_files():
    files = glob.glob(TEMP_FILE_DIR + "/*")
    for f in files:
        os.remove(f)
