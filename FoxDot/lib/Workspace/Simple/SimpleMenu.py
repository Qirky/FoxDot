import wx

class Menu(wx.MenuBar):
    def __init__(self, parent):
        wx.MenuBar.__init__(self)

        self.parent = parent

        # File Menu

        self.filemenu = wx.Menu()
        save_item = self.filemenu.Append(wx.ID_SAVE, "&Save", "Save your work")
        open_item = self.filemenu.Append(wx.ID_OPEN, "&Open", "Open a file in the editor")
        self.filemenu.AppendSeparator()
        exit_item  = self.filemenu.Append(wx.ID_EXIT,"E&xit"," Clock the program")

        self.parent.Bind(wx.EVT_MENU, self.OnSave, save_item)
        self.parent.Bind(wx.EVT_MENU, self.OnOpen, open_item)
        self.parent.Bind(wx.EVT_MENU, self.OnExit, exit_item)

        self.Append(self.filemenu, "&File")

    def OnSave(self, event):
        return self.parent.ctrl_save(event)

    def OnOpen(self, event):
        return self.parent.ctrl_open(event)

    def OnExit(self, event):
        return self.parent.kill()