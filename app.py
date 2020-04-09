import os

from fastapi import FastAPI
import uvicorn
from fastapi import UploadFile, File
from PIL import Image

app = FastAPI()
static_path = "/data/static/t-blog/"
static_url = "http://img.tonyiscoding.top"

def compress_img(file_name, com_level: int):
    img = Image.open(file_name)
    w, h = img.size
    new_img = img.resize((int(w / com_level), int(h / com_level)), Image.ANTIALIAS)
    new_img.save(file_name)

@app.post("/upload")
def upload_file(file: UploadFile = File(...), target: str = None):
    target_path = static_path + target
    if not os.path.exists(target_path):
        os.mkdir(target_path)
    file_name = target_path + "/" + file.filename
    image_bytes = file.file.read()
    image_len = len(image_bytes)
    with open(file_name, "wb") as f:
        f.write(image_bytes)
    if image_len > (400 * 1000):
        compress_img(file_name, 2)
    return {"status": "ok"}

@app.get("/list")
def get_file_list():
    file_dict = recursive_files(static_path, "/")
    return file_dict


def recursive_files(path: str, abs_path: str) -> dict:
    file_tree = dict()
    file_list = os.listdir(path)
    for file in file_list:
        next_file = path + "/" + file
        if os.path.isdir(next_file):  #  if is a directory
            file_tree[file] = recursive_files(next_file, abs_path + file + "/")
        else:
            file_tree[file] = static_url +  abs_path + file
    return file_tree


if __name__ == '__main__':
    uvicorn.run(app=app, port=9001)

