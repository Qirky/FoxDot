#!/usr/bin/env python
from __future__ import absolute_import

import sys
import wx

# Other widgets
from .SimpleText import Text
from .SimpleMenu import Menu

# FoxDot imports
from ...Settings import *
from ...Code import execute

class workspace:
    """ Wrapper for wxPython app """

    def __init__(self, CodeClass):

        self.app = wx.App(False)
        self.root = Editor(None, 'FoxDot - Live Coding with Python and SuperCollider')

    def run(self):
        """ Starts the wx mainloop for the master widget """
        while True:

            try:
                
                self.app.MainLoop()
                
                break

            # Temporary fix to unicode issues with Mac OS
            
            except(UnicodeDecodeError):
            
                pass
            
            except (KeyboardInterrupt, SystemExit):

                # Clean exit
                
                execute("Clock.stop()")
                execute("Server.quit()")
                
                break

class Editor(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(960*1.5,540*1.5))

        self.text = Text(self, style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER | wx.TE_RICH2 | wx.TE_CHARWRAP)

        # Cmd+H closes MacOS apps

        self.help_key = "K" if SYSTEM == MAC_OS else "H"

        # Key bindings

        shortcut_id = [wx.NewId() for n in range(10)]

        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL,  ord("\n"), shortcut_id[0] ),
            (wx.ACCEL_ALT,   ord("\n"), shortcut_id[1] ),
            (wx.ACCEL_CTRL,  ord("."),  shortcut_id[2] ),
            (wx.ACCEL_CTRL,  ord(self.help_key.lower()), shortcut_id[3] ),
            (wx.ACCEL_CTRL,  ord("s"), shortcut_id[4] ),
            (wx.ACCEL_CTRL,  ord("o"), shortcut_id[5] ),
            ]
        )

        self.SetAcceleratorTable(accel_tbl)

        # Bindings
        self.Bind(wx.EVT_MENU, self.ctrl_return, id=shortcut_id[0])
        self.Bind(wx.EVT_MENU, self.alt_return,  id=shortcut_id[1])
        self.Bind(wx.EVT_MENU, self.ctrl_period, id=shortcut_id[2])
        self.Bind(wx.EVT_MENU, self.ctrl_help,   id=shortcut_id[3])
        self.Bind(wx.EVT_MENU, self.ctrl_save,   id=shortcut_id[4])
        self.Bind(wx.EVT_MENU, self.ctrl_open,   id=shortcut_id[5])

        # Console and status bar
        self.console = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.CreateStatusBar()

        # Set font

        mono_font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.text.SetFont(mono_font)
        self.console.SetFont(mono_font)

        # Set up sizer grid
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.text, 2, wx.EXPAND)
        self.sizer.Add(self.console, 1, wx.EXPAND)

        # Layout grid
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        # self.sizer.Fit(self)

        # Forward sys.stdout to the console
        sys.stdout = self.console

        # Set menu

        self.menu_bar = Menu(self)
        self.SetMenuBar(self.menu_bar)

        self.Show(True)

        self.hello()

    def kill(self):
        """ Close the editor """
        return self.Close(True)

    def hello(self):
        """ Show welcome message """      

        if SYSTEM == MAC_OS:

            ctrl = "Cmd"
        
        else:
        
            ctrl = "Ctrl"
        
        hello = "Welcome to FoxDot! Press {}+{} for help.".format(ctrl, self.help_key)
        
        print(hello)
        
        print("-" * len(hello))

        return

    def flash(self, start, end):
        """ Highlight block of code and schedule de-highlight """
        self.text.highlight_block(start, end)
        return wx.CallLater(200, lambda: self.text.highlight_block(start, end, undo=True))

    # Binding

    def ctrl_return(self, event):
        """ Evaluates current block of code """
        start, end = self.text.get_current_block()
        code = self.text.get_block_text(start, end)
        if code:
            execute(code)
            self.flash(start, end)
        return

    def alt_return(self, event):
        """ Evaluates current line of code """
        row = self.text.get_current_row()
        code = self.text.get_block_text(row, row)
        if code:
            execute(code)
            self.flash(row, row)
        return

    def ctrl_period(self, event):
        """ Calls stop """
        return execute("Clock.clear()")

    def ctrl_help(self, event):
        """ Displays help message in console """
        if SYSTEM == MAC_OS:

            ctrl = "Cmd"
        
        else:
        
            ctrl = "Ctrl"
            
        print("FoxDot Help:")
        print("-----------------------------------------")
        print("{}+Return           : Execute code".format(ctrl))
        print("{}+.                : Stop all sound".format(ctrl))
        print("{}+S                : Save your work".format(ctrl))
        print("{}+O                : Open a file".format(ctrl))
        print("print(SynthDefs)      : View available SynthDefs")
        print("print(Samples)        : View character-to-sample mapping")
        print("print(FxList)         : View audio effects")
        print("print(Attributes)     : View Player attributes")
        print("print(PatternMethods) : View Pattern methods")
        print("---------------------------------------------------")
        print("Please visit foxdot.org for more information")
        print("---------------------------------------------------")
        return

    def ctrl_save(self, event):
        """ Save the contents in a .py file """
        with wx.FileDialog(self, "Save to disk",  wildcard="PY files (*.py)|*.py", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            # save the current contents in the file
            
            pathname = fileDialog.GetPath()
            
            try:
                with open(pathname, 'w') as file:
                    file.write(self.text.GetValue())
            except IOError:
                print("Cannot save file '%s'." % pathname)

    def ctrl_open(self, event):
        """ Open a file """
        with wx.FileDialog(self, "Open a file", wildcard="PY files (*.py)|*.py", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r') as file:
                    text = file.read()
                    self.text.SetValue(text)
            except IOError:
                print("Cannot open file '%s'." % pathname)
        return
