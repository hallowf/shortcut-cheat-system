import wx

from backend.backend_exceptions import CheatsMissing, ProcessError
from backend.scs_classes import Backend

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        # Backend stuff --------------------
        self.backend = None
        # Main components ------------------
        wx.Frame.__init__(self, parent, title=title, size=(500,600))
        self.CreateStatusBar() # A Statusbar in the bottom of the window
        panel = wx.Panel(self) # Main Panel
        self.SetBackgroundColour('grey')

        # Setting up the menu.
        filemenu = wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        menu_about = filemenu.Append(wx.ID_ABOUT, "&About","Information about this program")
        filemenu.AppendSeparator()
        menu_exit = filemenu.Append(wx.ID_EXIT,"&Exit","Terminate the program")

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
        self.logger = wx.TextCtrl(self, size=(300,200), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.logger.SetBackgroundColour((3, 62, 78))
        self.logger.SetForegroundColour((172, 180, 182))


        # add a spacer to the sizer
        grid.Add((10, 20), pos=(0,0))

        # Proccess name input
        self.proc_name = wx.StaticText(self, label="Process name:")
        self.proc_name.SetForegroundColour("MIDNIGHT BLUE")
        grid.Add(self.proc_name, pos=(1,0))
        self.proc_name_input = wx.TextCtrl(self, value="", size=(140,-1))
        grid.Add(self.proc_name_input, pos=(1,1))

        # Game input
        self.game_name = wx.StaticText(self, label="Game name:")
        self.game_name.SetForegroundColour("MIDNIGHT BLUE")
        grid.Add(self.game_name, pos=(2,0))
        self.game_name_input = wx.TextCtrl(self, value="", size=(140,-1))
        grid.Add(self.game_name_input, pos=(2,1))

        # Terminate command input
        self.end_command = wx.StaticText(self, label="Terminate shortcut:")
        self.end_command.SetForegroundColour("MIDNIGHT BLUE")
        grid.Add(self.end_command, pos=(3,0))
        self.end_command_input = wx.TextCtrl(self, value="Ex: p+e or esc", size=(140,-1))
        grid.Add(self.end_command_input, pos=(3,1))

        # another spacer
        grid.Add((10, 50), pos=(4,0))


        # Run button
        self.run_button = wx.Button(self, label="Run")
        self.Bind(wx.EVT_BUTTON, self.on_run,self.run_button)
        grid.Add(self.run_button, pos=(5,0))




        hSizer.Add(grid, 0, wx.ALL, 5)
        hSizer.Add(self.logger)
        mainSizer.Add(hSizer, 0, wx.ALL, 5)
        self.SetSizerAndFit(mainSizer)

        ## Events -------------------
        self.Bind(wx.EVT_MENU, self.on_about, menu_about)
        self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)



        # Show
        self.Show()


    def on_run(self,e):
        game_name = self.game_name_input.GetLineText(0)
        proc_name = self.proc_name_input.GetLineText(0)
        try:
            self.backend = Backend(game_name, proc_name, True)
            self.backend.find_cheats(game_name)
        except Exception as e:
            e_name = e.__class__.__name__
            e_str = ""
            if e_name == "CheatsMissing":
                e_str = "Failed to find cheats file"
            elif e_name == "KeyError":
                e_str = "Failed to found %s in cheats" % game_name
            elif e_name == "ProcessError":
                e_str = "Failed to access process %s" % proc_name
            else:
                e_str = str(e)
            self.logger.AppendText(e_str)

    def on_about(self, e):
        dlg = wx.MessageDialog( self, "SCS - Shortcut Cheat System, built with python and wxpython", "About SCS", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    # Exit method
    def on_exit(self,e):
        self.Close(True)
