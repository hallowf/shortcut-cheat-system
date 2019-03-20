import sys
import keyboard
import time
from backend.scs_classes import Backend

if __name__ == '__main__':
    do_exit = False
    try:
        b = Backend("Godfather", "pcsx2", "cheats.json", True)
        b.hook_keys()
        print("Running")
        keyboard.wait('esc')
        print("exiting")
        sys.exit(0)
    except Exception as e:
        raise e
