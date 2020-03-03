import wx, wx.html

# About modal
class AboutDialog(wx.Dialog): 
   def __init__(self, parent, title): 
      super(AboutDialog, self).__init__(parent, title = title, size = (500,250))
      panel = wx.Panel(self) # Panel
      # Sizers
      content_box = wx.BoxSizer(wx.VERTICAL)
      main_grid = wx.GridBagSizer(hgap=5, vgap=5)

      about_text = "\nSCS - Shortcut Cheat System\nbuilt with python and wxPython\n\n\n"
      warn_text = "Warning: This program makes no attempt to hide itself,\nso don't use it for online-play. Be responsible.\n\n\n"
      homepage = "Homepage\nhttps://github.com/hallowf/shortcut-cheat-system"
      about_text_ctrl = wx.TextCtrl(self, size=(450,240), style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_CENTRE)
      about_text_ctrl.AppendText(about_text)
      about_text_ctrl.AppendText(warn_text)
      about_text_ctrl.AppendText(homepage)

      self.ok_button = wx.Button(self, wx.ID_OK, label = "close")
      main_grid.Add(self.ok_button, pos=(0,0))
      # Add to content BoxSizer
      content_box.Add(about_text_ctrl)
      content_box.Add(main_grid, 0, wx.ALL, 5)
      self.SetSizerAndFit(content_box)


     

#Basic usage modal
class BasicUsageDialog(wx.Dialog): 
   def __init__(self, parent, title): 
      super(BasicUsageDialog, self).__init__(parent, title = title, size = (600,300))
      panel = wx.Panel(self) # Panel
      # Sizers
      content_box = wx.BoxSizer(wx.VERTICAL)
      main_grid = wx.GridBagSizer(hgap=5, vgap=5)

      # Not working
      BUD_not_working = "\nNot working?\n"
      BUD_not_working_help = "- First make sure all your vales correct\n"
      BUD_not_working_cheats = ""


      # Not working specific game
      BUD_specific_game = "\nSpecific game not working?\n"
      BUD_not_working_game = "Other applications, such as some games, may register hooks that swallow all key events.\n"

      # Requirements----------------------------------
      BUD_requirements = "\nRequirements:\n"
      BUD_requirements_proc = "Process name: This does not need the full name\n\tEX: notepad equals any process that has notepad in the name\n\n"
      BUD_requirements_cheats = "Cheats file: The location of your cheats file\n\tThis is the same for all systems\n\n"
      BUD_requirements_game = "Game name: The name of the game to load the cheats for\n\tThis is defined in the cheats file\n\n"
      BUD_requirements_shortcut = "Teminate shortcut: The shortcut to deactivate all shortcuts\n\tImportant: This does not close the app only removes shortcuts internally\n"

      # Windows ----------------------------------------
      BUD_windows = "\nOn Windows:\n"
      BUD_windows_proc = "Process name: Can be found on task manager\n"
      BUD_windows_limit = "Limitations:\n\t\tEvents generated under Windows don't report device id *(all keyboards connected are the same)\n"

      # Linux -------------------------------------------------
      BUD_linux = "\nOn Linux:\n"
      BUD_linux_root = "This app requires root permissions on linux explained below\n"
      BUD_linux_proc = 'Process name: Can be found in top/htop or ps -A | grep "name"\n'
      BUD_linux_limit = 'Limitations:\n\t\tMedia keys on Linux may appear nameless\n\tTo avoid depending on X, "keyboard" *(Python module) reads raw device files\n'
      help_text_ctrl = wx.TextCtrl(self, size=(600,350), style=wx.TE_MULTILINE | wx.TE_READONLY)

      titles=["BUD_not_working", "BUD_specific_game","BUD_requirements","BUD_windows","BUD_linux"]

      for symbol, value in locals().items():
         if symbol.startswith("BUD_"):
            if value.startswith("\n"):
               value = value.replace("\n", "\n\t", 1)
            if symbol in titles:
               help_text_ctrl.SetForegroundColour((172, 180, 182))
            help_text_ctrl.AppendText("\t"+value)
            help_text_ctrl.SetForegroundColour("white")

      # about_text_ctrl.AppendText(about_text)
      # about_text_ctrl.AppendText(warn_text)
      # about_text_ctrl.AppendText(homepage)

      self.ok_button = wx.Button(self, wx.ID_OK, label = "close")
      main_grid.Add(self.ok_button, pos=(0,0))
      # Add to content BoxSizer
      content_box.Add(help_text_ctrl)
      content_box.Add(main_grid, 0, wx.ALL, 5)
      self.SetSizerAndFit(content_box)