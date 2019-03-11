import wx

from backend.exceptions import CheatsMissing, ProcessError

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        # Main components ------------------
        wx.Frame.__init__(self, parent, title=title, size=(500,600))
        self.CreateStatusBar() # A Statusbar in the bottom of the window
        panel = wx.Panel(self) # Main Panel
        self.SetBackgroundColour('white')

        # Setting up the menu.
        filemenu = wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        menu_about = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        filemenu.AppendSeparator()
        menu_exit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        # Creating the menubar.
        menu_bar = wx.MenuBar()
        menu_bar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menu_bar)  # Adding the MenuBar to the Frame content.


        ## Content ---------------------

        # create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(hgap=5, vgap=5)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)



        # Logger
        self.logger = wx.TextCtrl(self, size=(200,200), style=wx.TE_MULTILINE | wx.TE_READONLY)

        # add a spacer to the sizer
        grid.Add((10, 20), pos=(0,0))

        # the edit control - one line version.
        self.lblname = wx.StaticText(self, label="Game name :")
        grid.Add(self.lblname, pos=(1,0))
        self.game_name = wx.TextCtrl(self, value="Enter here your name", size=(140,-1))
        grid.Add(self.game_name, pos=(1,1))

        # another spacer
        grid.Add((10, 20), pos=(2,0))


        # Run button
        self.button = wx.Button(self, label="Run")
        self.Bind(wx.EVT_BUTTON, self.on_run,self.button)




        hSizer.Add(grid, 0, wx.ALL, 5)
        hSizer.Add(self.logger)
        mainSizer.Add(hSizer, 0, wx.ALL, 5)
        mainSizer.Add(self.button, 0, wx.CENTER)
        self.SetSizerAndFit(mainSizer)

        ## Events -------------------
        self.Bind(wx.EVT_MENU, self.on_about, menu_about)
        self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)



        # Show
        self.Show()


    def on_run(self,e):
        print(1)

    def on_about(self, e):
        dlg = wx.MessageDialog( self, "SCS - Shortcut Cheat System, built with python and wxpython", "About SCS", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    # Exit method
    def on_exit(self,e):
        self.Close(True)
