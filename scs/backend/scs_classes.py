import json
import time
import os
import sys

import psutil
import keyboard

from .exceptions import CheatsMissing, ProcessError

class Backend(object):
    """Requires game name and cheats
       Cheats are a dict with hotkey, address and value"""
    def __init__(self, game_name, check=False):
        super(Backend, self).__init__()
        if check:
            try:
                Checker().run_all()
            except (ProcessError, CheatsMissing) as e:
                raise e
        cp = None
        try:
            cp = CheatsParser(game_name)
        except (JSONDecodeError, FileNotFoundError, KeyError) as e:
            raise e
        cheats = cp.game_cheats
        self.game_name = game_name
        self.cheats = cheats
        self.combs = [comb.lower() for comb in cheats]

    def hook_hotkeys(self):
        self.handles = []
        for comb in self.combs:
            a = keyboard.add_hotkey(comb, print, args=(self.cheats[comb][0], self.cheats[comb][1]))
            self.handles.append(a)
        # TODO: this does not seem to work with keyboard.wait(key)
        # maybe use wait within class
        # exit_handle = keyboard.add_hotkey("ctrl+p+e", sys.exit, args=(0))
        # self.handles.append(exit_handle)


    def unhook_keys(self):
        keyboard.unhook_all_hotkeys()

    def __exit__(self):
        keyboard.unhook_all_hotkeys()



class Checker(object):

    def __init__(self):
        self.restarts = 0

    def check_cheats(self):
        if not os.path.isfile("cheats.json"):
            return False
        else:
            return True

    def check_proc(self):
    #Iterate over the all the running process
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            try:
                # Check if process name contains the given name string.
                if "pcsx2" in proc.info["name"].lower():
                    self.proc = proc
                    return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                time.sleep(5)
                if self.restarts >= 4:
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
    def __init__(self,game_name):
        self.game_name = game_name
        try:
            with open("cheats.json", "r") as f:
                try:
                    self.cheats = json.load(f)
                except Exception as e:
                    raise e
        except FileNotFoundError:
            raise FileNotFoundError
        try:
            self.game_cheats = self.find_cheats(self.game_name)
        except KeyError:
            raise KeyError

    def find_cheats(self, game_name):
        try:
            return self.cheats[game_name]
        except KeyError:
            raise KeyError
