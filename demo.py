import os
from PIL import Image


def compress_img(file_name):
    img = Image.open(file_name)
    w, h = img.size
   #new_img = img.resize((int(w / 4), int(h / 4)), Image.ANTIALIAS)
   #new_img.save(file_name)


if __name__ == '__main__':
    compress_img("/data/sites/file_upload/part_and_cg.png")

