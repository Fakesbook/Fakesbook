import sys
import os

def get_absolute_path(relative_path):

    try:
        path = sys._MEIPASS
    except Exception:
        path = os.path.abspath('.')

    return os.path.join(path, relative_path)
