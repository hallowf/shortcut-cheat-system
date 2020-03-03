import json
import time
import os
import sys
import platform
import string
import logging

import psutil
import keyboard

from .backend_exceptions import CheatsMissing, ProcessError, InvalidShortcut
# Due to my terrible c type conversion
# writter args on windows writter(string: pid, int: address, int: value)
# writter args on linux writter(int: pid, int: address, int: value)
from .c_writter import writter

class Backend(object):
    """----------------------------------------------------
        Requires process name, cheats file and end combination.
        Process name does not require the full name.
        Cheats are a json dict with: "hotkey": [address, value].
        end combination is a string with the keys to be pressed
        for the listener to stop Ex: "ctrl+p+e".
    -------------------------------------------------------"""
    def __init__(self, p_name, cheats_file, end_comb, check=True, **kwargs):
        super(Backend, self).__init__()
        self.system = "windows" if platform.system().lower() == "windows" else "linux"
        if check:
            try:
                p_info = Checker(cheats_file,p_name).run_all()
                self.pid = p_info.info["pid"]
            except (ProcessError, CheatsMissing) as e:
                raise e
        cf = None
        try:
            cf = CheatsFileParser(cheats_file, end_comb).return_cheats()
        except (InvalidShortcut, KeyError, Exception) as e:
            raise e
        self.p_name = p_name
        self.cheats = cf
        self.hooked = False
        self.end_comb = end_comb
        self.list_shortcuts_key = kwargs.get("list_shortcuts_key", "ctrl+i")
        self.log_level = kwargs.get("log_level")
        self.logger = self.install_logger()

    def install_logger(self):
        n_level = getattr(logging, self.log_level.upper(), 10)
        # Console logger
        log_format = "%(name)s - %(levelname)s: %(message)s"
        logging.basicConfig(format=log_format, level=n_level)
        logger = logging.getLogger("SCS-Backend")
        msg = "%s: %s" % ("Console logger is set with log level", self.log_level)
        logger.info(msg)
        return logger

    # Show key combinations
    def show_combs(self):
        combs = [comb.lower() for comb in self.cheats]
        self.logger.info("Available shortcuts: %s" % combs)
        

    # For hoooking the hotkeys found in cheats.json
    def hook_keys(self):
        self.logger.info("hooking keys")
        game_cheats = self.cheats
        combs = [comb.lower() for comb in game_cheats]
        for comb in combs:
            keyboard.add_hotkey(comb, self.func_hotkey, args=(game_cheats[comb][1],game_cheats[comb][0]))
        # hotkey for showing combinations
        keyboard.add_hotkey(self.list_shortcuts_key, self.show_combs, args=())
        self.hooked = True

    # function to run and wait for the end combination
    # unhooks all keys after
    def run(self):
        keyboard.wait(self.end_comb)
        keyboard.unhook_all_hotkeys()

    # executes the memory writter plugin according to the current OS
    def func_hotkey(self, val, addr):
        if self.system == "windows":
            self.logger.debug("Writting: ", val, " at ", addr, " on process ", str(self.pid))
            writter(str(self.pid), int(addr, 0), val)
        elif self.system == "linux":
            self.logger.debug("Writting: ", val, " at ", addr, " on process ", str(self.pid))
            writter(self.pid, int(addr, 0), val)

    # Unhooks all hotkeys
    def unhook_keys(self):
        keyboard.unhook_all_hotkeys()

    # For unexpected exits
    def __exit__(self, tp, val, tb):
        keyboard.unhook_all_hotkeys()

class Checker(object):
    """
    Used for verifying the existence of the cheats file and the process
    """

    def __init__(self, cheats_file, p_name):
        self.restarts = 0
        self.cheats_file = cheats_file
        self.p_name = p_name
        self.proc = None

    # check existence of cheats file
    def check_cheats_file(self):
        if not os.path.isfile(self.cheats_file):
            return False
        else:
            return True

    # check existence of process
    def check_proc(self):
    #Iterate over the all the running processes
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            try:
                # Check if process name contains the given name string.
                if self.p_name.lower() in proc.info["name"].lower():
                    self.proc = proc
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                time.sleep(3)
                if self.restarts > 3 or self.restarts < 0:
                    return False
                else:
                    self.restarts = self.restarts + 1
                    self.check_proc()
        return False

    # this should have a better name since it also 
    # returns the process info if all checks pass
    def run_all(self):
        if not self.check_cheats_file():
            raise CheatsMissing
        elif not self.check_proc():
            raise ProcessError
        else:
            return self.proc

class CheatsFileParser(object):
    """
    Used for verifying the shortcuts and appending 0x to the memory address of the cheats
    """
    def __init__(self, cheats_file, end_comb):
        self.cheats = None
        with open(cheats_file, "r") as f:
            try:
                self.cheats = json.load(f)
            except Exception as e:
                raise e
        self.shortcuts = [shortcut for shortcut in self.cheats]
        self.shortcuts.append(end_comb)
        try:
            self.verify_shortcuts()
        except InvalidShortcut as e:
            raise e
        self.fix_addresses()

    # returns parsed cheats
    def return_cheats(self):
        return self.cheats

    # Iterates trough each shortcut finds all cheats and adds 0x to the address
    def fix_addresses(self):
        for key in self.cheats:
            if not self.cheats[key][0].startswith("0x"):
                self.cheats[key][0] = "0x%s" % self.cheats[key][0]
    
    # Verifies all shortcuts provided in cheats file
    def verify_shortcuts(self):
        for shortcut in self.shortcuts:
            shortcut = shortcut.lower()
            if shortcut.startswith("+") or shortcut.endswith("+"):
                raise InvalidShortcut(shortcut)
            else:
                short_keys = shortcut.split("+")
                possible_keys = list(string.ascii_letters)
                possible_numbers = [str(i) for i in range(10)]
                special_keys = ["ctrl","shift","tab","home","insert","end","delete","pause", "esc"]
                possible_keys.extend(possible_numbers)
                possible_keys.extend(special_keys)
                for key in short_keys:
                    if key not in possible_keys:
                        raise InvalidShortcut(key)
