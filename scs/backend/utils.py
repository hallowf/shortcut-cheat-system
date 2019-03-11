
class KeystrokeCheatMapper(object):
    """docstring for KeystrokeCheatMapper."""
    def __init__(self):
        super(KeystrokeCheatMapper, self).__init__()
        self.current_comb = []
        self.exit_comb = ["CTRL_L", "P", "E"]
        self.exit_comb = [key.upper() for key in self.exit_comb]

    def on_press(self, key):
        try:
            k_str = str(key.char).upper()
            self.current_comb.append(k_str.upper())
        except AttributeError:
            k_str = str(key.name).upper()
            self.current_comb.append(k_str)

    def on_release(self, key):
        if self.current_comb == self.exit_comb:
            # Stop listener
            return False
        self.current_comb = [] if self.current_comb != [] else self.current_comb
