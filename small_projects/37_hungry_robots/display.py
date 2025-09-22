import os
import sys


def clear_screen(clear: str = "cls" if sys.platform == "win32" else "clear"):
    os.system(clear)
