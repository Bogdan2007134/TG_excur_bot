import sys
# sys.path.append(r'C:\Users\user\Desktop\excur_bot(stability)')
from print_colorama import *

async def read_txt_file(file_name):
    contents = []
    # for file_name in file_names:
    try:
        with open(file_name, encoding='utf-8') as file:
            read = file.read()
            contents = read
    except FileNotFoundError:
        error('Ошибка при чтении файла!!!')
        print(f"Файл '{file_name}' не найден.")
    except Exception as e:
        error('Ошибка при чтении файла!!!')
        print(f"Произошла ошибка при чтении файла '{file_name}': {str(e)}")
    return contents

