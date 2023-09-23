async def read_txt_file(file_names):
    contents = []
    for file_name in file_names:
        try:
            with open(file_name, encoding="utf-8") as file:
                read = file.read()
                contents.append(read)
        except FileNotFoundError:
            print(f"Файл '{file_name}' не найден.")
        except Exception as e:
            print(f"Произошла ошибка при чтении файла '{file_name}': {str(e)}")
    return contents


# contents = await read_txt.read_txt_file(['maintxt\\help.txt'])
# print(contents)
