import os.path
import secrets
from flask import current_app
from PIL import Image

def save_scan(scan):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(scan.filename)
    scan_fn = random_hex + f_ext
    scan_path = os.path.join(current_app.config['SERVER_PATH'], scan_fn)

    #Для сохранения картинки
    output_size = (125, 125)
    i = Image.open(scan)
    i.thumbnail(output_size)
    i.save(scan_path)
    return scan_fn

