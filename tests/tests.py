# import base64


# with open("tests/234.jpg", "rb") as image_file:
#     encoded_string = base64.b64encode(image_file.read())
#     print(encoded_string)
import random
def get_promo_code(num_chars):
    code_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code = ""
    for i in range(0, num_chars):
        slice_start = random.randint(0, len(code_chars) - 1)
        code += code_chars[slice_start : slice_start + 1]
    return code

print(get_promo_code(20))