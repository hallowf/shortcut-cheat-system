import wx, keyboard, pickle, os

from backend.backend_exceptions import CheatsMissing, ProcessError
from backend.scs_classes import Backend
from backend.utils import KeyListener, verify_shortcut
from wx._core import StaticText

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        # Backend stuff ----------------------------------
        self.scs_backend = None
        self.cheats_file_path = None
        self.keys_hooked = None
        self.keyboard_hook = None
        # Main components ---------------------------------
        wx.Frame.__init__(self, parent, title=title, size=(500,600))
        self.CreateStatusBar() # A Statusbar in the bottom of the window
        panel = wx.Panel(self) # Main Panel
        self.SetBackgroundColour('grey')

        # Setting up the menu.
        filemenu = wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        menu_about = filemenu.Append(wx.ID_ABOUT, "&About","Information about this program")
        menu_save = filemenu.Append(wx.ID_SAVE, '&Save', "Save current values")
        filemenu.AppendSeparator()
        menu_exit = filemenu.Append(wx.ID_EXIT,"&Exit","Terminate the program")

        # Creating the menubar.
        menu_bar = wx.MenuBar()
        menu_bar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menu_bar)  # Adding the MenuBar to the Frame content.


        ## Content ---------------------------------------

        # create some sizers
        content_box = wx.BoxSizer(wx.VERTICAL)
        main_grid = wx.GridBagSizer(hgap=5, vgap=5)
        button_grid = wx.GridBagSizer(hgap=20, vgap=1)
        main_box = wx.BoxSizer(wx.HORIZONTAL)

        ## main_grid -----------------------------------
        # Logger
        self.logger = wx.TextCtrl(self, size=(300,225), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.logger.SetBackgroundColour((3, 62, 78))
        self.logger.SetForegroundColour((172, 180, 182))

        # add a spacer to the sizer
        main_grid.Add((10, 20), pos=(0,0))

        # Proccess name input
        self.proc_name = wx.StaticText(self, label="Process name:")
        self.proc_name.SetForegroundColour("MIDNIGHT BLUE")
        main_grid.Add(self.proc_name, pos=(1,0))
        self.proc_name_input = wx.TextCtrl(self, value="", size=(140,-1))
        main_grid.Add(self.proc_name_input, pos=(1,1))

        # Cheats file
        self.cheats_file = wx.StaticText(self, label="Cheats file:")
        self.cheats_file.SetForegroundColour("MIDNIGHT BLUE")
        main_grid.Add(self.cheats_file, pos=(2,0))
        self.cheats_file_input = wx.Button(self, label="Open")
        main_grid.Add(self.cheats_file_input, pos=(2,1))

        # Game input
        self.game_name = wx.StaticText(self, label="Game name:")
        self.game_name.SetForegroundColour("MIDNIGHT BLUE")
        main_grid.Add(self.game_name, pos=(3,0))
        self.game_name_input = wx.TextCtrl(self, value="", size=(140,-1))
        main_grid.Add(self.game_name_input, pos=(3,1))
        
        # Terminate command input
        self.end_comb = wx.StaticText(self, label="Terminate shortcut:")
        self.end_comb.SetForegroundColour("MIDNIGHT BLUE")
        main_grid.Add(self.end_comb, pos=(4,0))
        self.end_comb_input = wx.TextCtrl(self, value="Ex: p+e or esc", size=(140,-1))
        main_grid.Add(self.end_comb_input, pos=(4,1))

        ## button_grid -----------------------------------
        # Hook button
        self.hook_button = wx.Button(self, label="Hook")
        button_grid.Add(self.hook_button, pos=(1,0))

        # Unhook button
        self.unhook_button = wx.Button(self, label="Unhook")
        button_grid.Add(self.unhook_button, pos=(1,1))

        # add a spacer between button
        button_grid.Add((55, 10), pos=(1,2))

        # Clean log button
        self.clean_button = wx.Button(self, label="Clean")
        button_grid.Add(self.clean_button, pos=(1,3))

        # Test key logging
        self.test_key = wx.Button(self, label="Test keys")
        button_grid.Add(self.test_key, pos=(1,4))

        # Add everything to content_box
        main_box.Add(main_grid, 0, wx.ALL, 5)
        main_box.Add(self.logger)
        content_box.Add(main_box, 0, wx.ALL, 5)
        content_box.Add(button_grid, 0, wx.ALL, 5)
        self.SetSizerAndFit(content_box)

        ## Events -------------------
        ## Menus
        self.Bind(wx.EVT_MENU, self.on_about, menu_about)
        self.Bind(wx.EVT_MENU, self.on_save, menu_save)
        self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)
        ## Buttons
        self.Bind(wx.EVT_BUTTON, self.on_open_cheats, self.cheats_file_input)
        self.Bind(wx.EVT_BUTTON, self.on_hook,self.hook_button)
        self.Bind(wx.EVT_BUTTON, self.on_unhook,self.unhook_button)
        self.Bind(wx.EVT_BUTTON, self.on_clean,self.clean_button)
        self.Bind(wx.EVT_BUTTON, self.on_test,self.test_key)

        ## Check for stored settings
        if os.path.isfile("settings.pckl") and os.path.getsize("settings.pckl") > 0:
            with open("settings.pckl", "rb") as pckl:
                to_load = pickle.load(pckl)                     
                if to_load["game_name"]:
                    self.game_name_input.SetValue(to_load["game_name"])
                if to_load["proc_name"]:
                    self.proc_name_input.SetValue(to_load["proc_name"])
                if to_load["end_comb"]:
                    self.end_comb_input.SetValue(to_load["end_comb"])
                if to_load["cheats_file"]:
                    self.cheats_file_path = to_load["cheats_file"]

        # Show
        self.Show()

    # File dialog for cheats file
    def on_open_cheats(self, e):
         # otherwise ask the user what new file to open
        with wx.FileDialog(self, "Open cheats file", wildcard=".json files (*.json)|*.json",
                        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind
            # get the path
            self.cheats_file_path = fileDialog.GetPath()
        self.logger.AppendText("Path of cheats file is:\n%s\n" % self.cheats_file_path)

    # Check user inputs
    def check_inputs(self):
        inputs = {}
        game_name = self.game_name_input.GetLineText(0).strip()
        proc_name = self.proc_name_input.GetLineText(0).strip()
        end_comb = self.end_comb_input.GetLineText(0).strip()
        inputs.update({
            "Game name":game_name,
            "Process name":proc_name,
            "Cheats file":self.cheats_file_path
            })
        for value in inputs:
            if not inputs[value] or inputs[value] == "" or inputs[value] == " " or isinstance(inputs[value], StaticText):
                self.logger.AppendText("Missing value: %s\n" % value)
                return False
        if not verify_shortcut(end_comb):
            return False
        return True

    # To rehook hotkeys
    def on_re_hook(self,e):
        game_name = self.game_name_input.GetLineText(0).strip()
        if not self.scs_backend:
            self.logger.AppendText("Keyboard not hooked..\n")
        else:
            self.logger.AppendText('"Re-hooking" shortcuts\n')
            self.scs_backend.re_hook_keys(game_name)

    # This unhooks the keyboard and terminates the backend
    def on_unhook(self,e):
        if not self.scs_backend:
            self.logger.AppendText("Keyboard not hooked..\n")
        else:
            self.logger.AppendText('"Un-hooking" shortcuts and terminating backend\n')
            self.scs_backend.unhook_keys()
            self.scs_backend = None

    # To hook the keyboard
    def on_hook(self,e):
        if not self.check_inputs():
            return
        game_name = self.game_name_input.GetLineText(0).strip()
        proc_name = self.proc_name_input.GetLineText(0).strip()
        end_comb = self.end_comb_input.GetLineText(0).strip()
        try:
            self.logger.AppendText("Starting backend, parameters:\n\tProcess:%s\n\tGame name:%s\n" % (proc_name, game_name))
            self.scs_backend = Backend(proc_name, self.cheats_file_path, game_name, end_comb)
            self.scs_backend.hook_keys()
        except Exception as e:
            e_name = e.__class__.__name__
            e_str = ""
            if e_name == "CheatsMissing":
                e_str = "Failed to find cheats file at %s\n" % self.cheats_file_path
            elif e_name == "KeyError":
                e_str = "Failed to found %s in cheats\n" % game_name
            elif e_name == "ProcessError":
                e_str = "Failed to access process %s\n" % proc_name
            else:
                e_str = str(e)
            self.logger.AppendText(e_str + "\n")

    def on_clean(self,e):
        self.logger.SetValue("")

    def on_test(self,e):
        if self.keys_hooked:
            self.logger.AppendText("Unhooking keys\n")
            if self.keyboard_hook:
                try:
                    keyboard.unhook(self.keyboard_hook)
                    self.logger.AppendText("Unhooked\n")
                    self.keys_hooked = False
                except KeyError:
                    self.logger.AppendText("Failed to unhook listener, unhooking all keyboard listeners\n") 
                    keyboard.unhook_all()
                    self.keys_hooked = False
            else:
                self.logger.AppendText("Failed to find hook, unhooking all keyboard listeners\n")
                keyboard.unhook_all()
                self.keys_hooked = False
        else:
            self.logger.AppendText("Hooking keys\n")
            self.logger.AppendText("There is a 0.14 second delay plus the time it takes to write text to here\nThe delay only aplies to this test.")
            self.logger.AppendText("If you spam the keyboard this will probably lag or crash....\n")
            self.keys_hooked = True
            listener = KeyListener(self.logger)
            self.keyboard_hook = keyboard.hook(listener.log_key)


    def on_about(self, e):
        dlg = wx.MessageDialog( self, "SCS - Shortcut Cheat System, built with python and wxpython", "About SCS", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def on_save(self,e):
        game_name = self.game_name_input.GetLineText(0).strip()
        proc_name = self.proc_name_input.GetLineText(0).strip()
        end_comb = self.end_comb_input.GetLineText(0).strip()
        self.logger.AppendText("Saving values:\n\tGame name:%s\n\tProcess:%s\n\tEnd command:%s\n\tCheats file:%s\n" % (game_name, proc_name, end_comb, self.cheats_file_path))
        to_save = {
            "game_name": game_name,
            "proc_name": proc_name,
            "end_comb": end_comb,
            "cheats_file": self.cheats_file_path
            }
        with open("settings.pckl", "wb") as pckl:
            pickle.dump(to_save, pckl, protocol=pickle.HIGHEST_PROTOCOL)
        pckl_path = os.path.abspath("settings.pckl")
        self.logger.AppendText("Wrote file at:\n\t%s" % pckl_path)

    # Exit method
    def on_exit(self,e):
        keyboard.unhook_all()
        self.Close(True)
