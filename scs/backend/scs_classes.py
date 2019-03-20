import json
import time
import os
import sys
import platform

import psutil
import keyboard

from .backend_exceptions import CheatsMissing, ProcessError
# Due to my terrible c type conversion
# writter args on windows writter(string: pid, int: address, int: value)
# writter args on linux writter(int: pid, int: address, int: value)
from .c_writter import writter

class Backend(object):
    """----------------------------------------------------
        Requires process name game name and cheats file
        Process name does not require the full name
        Cheats are a dict with hotkey, address and value
        game name can be overriden by simply:
            Backend.re_hook_keys("new_name")
        if the game is not found this raises a KeyError
    -------------------------------------------------------"""
    def __init__(self, p_name, cheats_file, game_name, check=True):
        super(Backend, self).__init__()
        self.system = "windows" if platform.system().lower() == "windows" else  "linux"
        if check:
            try:
                p_info = Checker(cheats_file,p_name).run_all()
                self.pid = p_info.info["pid"]
            except (ProcessError, CheatsMissing) as e:
                raise e
        cp = None
        try:
            cp = CheatsParser(cheats_file)
            cp.cheats[game_name]
        except (FileNotFoundError, KeyError, Exception) as e:
            raise e
        self.game_name = game_name
        self.cheats = cp.cheats
        self.hooked = False
        

    # For hoooking the hotkeys found in cheats.json
    def hook_hotkeys(self):
        handles = []
        game_cheats = self.cheats[self.game_name]
        combs = [comb.lower() for comb in game_cheats]
        for comb in combs:
            a = keyboard.add_hotkey(comb, self.func_hotkey, args=(comb, game_cheats[comb]))
            handles.append(a)
        self.handles = handles
        self.hooked = True
        # TODO: this does not seem to work with keyboard.wait(key)
        # exit_handle = keyboard.add_hotkey("ctrl+p+e", sys.exit, args=(0))
        # self.handles.append(exit_handle)

    def func_hotkey(self, key, value_s):
        if isinstance(value_s[0], list):
            for val in value_s:
                if self.system == "windows":
                    writter(str(self.pid), int(val[0], 0), val[1])
                elif self.system == "linux":
                    writter(self.pid, int(val[0], 0), val[1])
        else:
            if self.system == "windows":
                writter(str(self.pid), int(val[0], 0), val[1])
            elif self.system == "linux":
                writter(self.pid, int(val[0], 0), val[1])

    def re_hook_keys(self, new_game):
        if self.hooked:
            self.unhook_keys()
        self.game_name = new_game
        try:
            self.cheats[self.game_name]
        except KeyError as e:
            raise e
        self.hook_hotkeys()

    # Unhooks all hotkeys
    def unhook_keys(self):
        keyboard.unhook_all_hotkeys()
        self.handles = []

    def __exit__(self, tp, val, tb):
        keyboard.unhook_all_hotkeys()

class Checker(object):

    def __init__(self, cheats_file, p_name):
        self.restarts = 0
        self.p_name = p_name
        self.cheats_file = cheats_file

    def check_cheats(self):
        if not os.path.isfile(self.cheats_file):
            return False
        else:
            return True

    def check_proc(self):
    #Iterate over the all the running process
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            try:
                # Check if process name contains the given name string.
                if self.p_name in proc.info["name"].lower():
                    self.proc = proc
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                time.sleep(3)
                if self.restarts > 3 or self.restarts < 0:
                    return False
                else:
                    self.restarts = self.restarts + 1
                    self.check_proc()
        return False

    def run_all(self):
        if not self.check_cheats():
            raise CheatsMissing
        elif not self.check_proc():
            raise ProcessError
        else:
            return self.proc

class CheatsParser(object):
    """docstring for CheatsParser."""
    def __init__(self, cheats_file):
        try:
            with open(cheats_file, "r") as f:
                try:
                    self.cheats = json.load(f)
                except Exception as e:
                    raise e
        except FileNotFoundError:
            raise CheatsMissing
        self.fix_addresses()

    # Iterates trough each game finds all cheats and adds 0x to the address
    # in case the user forgot..
    def fix_addresses(self):
        for game in self.cheats:
            for key in self.cheats[game]:
                if isinstance(self.cheats[game][key][0], list):
                    for idx, cheat in enumerate(self.cheats[game][key]):
                        if not cheat[0].startswith("0x"):
                            self.cheats[game][key][idx][0] = "0x%s" % cheat[0]
                else:
                    if not self.cheats[game][key][0].startswith("0x"):
                        self.cheats[game][key][0] = "0x%s" % self.cheats[game][key][0]
