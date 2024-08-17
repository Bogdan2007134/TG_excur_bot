from colorama import Fore, Style
import sys


def error(text):
    print(Fore.RED + "[ERROR]", Style.RESET_ALL + str(text))


def info(text):
    print(Fore.GREEN + "[INFO]", Style.RESET_ALL + str(text))


def warning(text):
    print(Fore.YELLOW + "[WARNING]", Style.RESET_ALL + str(text))


def _warning(key, value):
    print(f'{key}:', Fore.YELLOW + "[ ", Style.RESET_ALL +
          str(value), Fore.YELLOW + " ]", Style.RESET_ALL + str(''))


def _informing(key, value):
    print(f'{key}:', Fore.GREEN + "[ ", Style.RESET_ALL +
          str(value), Fore.GREEN + " ]", Style.RESET_ALL + str(''))


def _informing_array(key, value):
    print(f'{key}:', Fore.GREEN +
          str(value), Style.RESET_ALL + str(''))


def _warning_array(key, value):
    print(f'{key}:', Fore.RED +
          str(value), Style.RESET_ALL + str(''))


def _close_dict(obj, color):
    print(color +
          str(obj), Style.RESET_ALL + str(''))


def refresh(text):
    print(Fore.LIGHTGREEN_EX + "[REFRESH]", Style.RESET_ALL + str(text))


def calculated_percent(x, y):
    if x == 0 or y == 0:
        return 0
    else:
        percentage = (x / y) * 100
        return percentage


color = [
    Fore.RED,
    Fore.BLUE,
    Fore.GREEN,
    Fore.MAGENTA,
    Fore.YELLOW,
    Fore.CYAN,
    Fore.RED,
    Fore.BLUE,
    Fore.GREEN,
    Fore.MAGENTA,
    Fore.YELLOW,
    Fore.CYAN,
    Fore.RED,
    Fore.BLUE,
    Fore.GREEN,
    Fore.MAGENTA,
    Fore.YELLOW,
    Fore.CYAN,
    Fore.WHITE]


def object_print(name_data, data):
    info('Data a ' + name_data + ':')
    right_data = 0
    global_data = 0
    for key, value in data.items():
        if value != '' and value != None:
            right_data += 1
            global_data += 1

            _informing(key, value)
        else:
            global_data += 1
            _warning(key, 'data undefined')
    info(f'Data right a {int(calculated_percent(right_data,global_data))}%')


def process_dict(data):
    indent = 0
    col = 0
    right_data = 0
    global_data = 0
    info('Weight in Kilobyte ' + str(sys.getsizeof(data)/1024))
    _close_dict((indent * ' ') + "{", color[col])

    def _process_dict(data):
        nonlocal right_data, global_data, indent, col
        for key, value in data.items():
            if isinstance(value, dict):
                col += 1
                _close_dict((indent * ' ') + key+" :{", color[col])
                indent += 4
                _process_dict(value)
            else:
                if value != '' and value != None:
                    right_data += 1
                    global_data += 1
                else:
                    global_data += 1
                print(f"{indent * ' '}{key} : {value}")
        indent -= 4
        _close_dict((indent * ' ') + ' },', color[col])
        col -= 1
    _process_dict(data)
    info(f'Data right a {int(calculated_percent(right_data,global_data))}%')

def products_Print(data):
    indent = 0
    col = 0
    right_data = 0
    global_data = 0
    info('Weight in Kilobyte ' + str(sys.getsizeof(data)/1024))
    for _data in data['products']:
        _close_dict((indent * ' ') + "{", color[col])

        def _products_Print(data):
            nonlocal right_data, global_data, indent, col
            for key, value in data.items():
                if isinstance(value, dict):
                    col += 1
                    _close_dict((indent * ' ') + key+" :{", color[col])
                    indent += 4
                    _products_Print(value)
                else:
                    if value != '' and value != None:
                        right_data += 1
                        global_data += 1
                    else:
                        global_data += 1
                    print(f"{indent * ' '}{key} : {value}")
            indent -= 4
            _close_dict((indent * ' ') + '},', color[col])
            col -= 1
        _products_Print(_data)
        info(f'Data right a {int(calculated_percent(right_data,global_data))}%')


