import wx
from gui.home import MainWindow

def run_main():
    app = wx.App(False)
    frame = MainWindow(None, "SCS - Shortcut Cheat System")
    app.MainLoop()




if __name__ == '__main__':
    run_main()
