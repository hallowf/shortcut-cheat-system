import sys
import keyboard
import time
from backend.scs_classes import Backend

if __name__ == '__main__':
    do_exit = False
    try:
        b = Backend("pcsx2", "cheats.json", "Godfather",  "ctrl+p+e", True)
        b.hook_keys()
        print("Running...\nPress ctrl+p+e or esc to exit")
        keyboard.wait('esc')
        print("exiting")
        sys.exit(0)
    except Exception as e:
        raise e
