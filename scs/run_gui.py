import wx
from gui.main_gui import MainWindow

from .run_back import run_back

def run_main():
    app = wx.App(False)
    frame = MainWindow(None, "SCS - Shortcut Cheat System")
    app.MainLoop()




if __name__ == '__main__':
    run_main()
