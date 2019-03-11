import sys
import keyboard
import time
from backend.scs_classes import Backend

if __name__ == '__main__':
    do_exit = False
    try:
        b = Backend("Godfather")
        b.hook_hotkeys()
        print("Running")
        keyboard.wait('esc')
        print("exiting")
        sys.exit(0)
    except Exception as e:
        raise e
        sys.exit(1)
