import random
from config.config import settings
import base64
import cv2
import numpy as np

def correct_padding(data):
    missing_padding = len(data) % 4
    if missing_padding:
        data += "=" * (4 - missing_padding)
    return data


async def save_img(encoded_data, filename):
    encoded_data = correct_padding(encoded_data)
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return cv2.imwrite(filename, img)

def get_promo_code(num_chars):
     code_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
     code = ''
     for i in range(0, num_chars):
         slice_start = random.randint(0, len(code_chars) - 1)
         code += code_chars[slice_start: slice_start + 1]
     return code