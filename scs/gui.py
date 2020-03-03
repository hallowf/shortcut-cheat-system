import wx, sys
from gui.home import MainWindow

def run_main():
    app = wx.App(False)
    frame = MainWindow(None, "SCS - Shortcut Cheat System")
    icon = wx.Icon()
    icon.CopyFromBitmap(wx.Bitmap("scs.ico", wx.BITMAP_TYPE_ANY))
    frame.SetIcon(icon)
    frame.Center()
    frame.Show()
    app.MainLoop()




if __name__ == '__main__':
    sys.stdout.write("Starting SCS GUI\n")
    run_main()
