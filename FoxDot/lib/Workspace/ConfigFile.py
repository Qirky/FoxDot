from __future__ import absolute_import, division, print_function

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

from ..Settings import FOXDOT_ICON, FOXDOT_ICON_GIF

try:
    import tkMessageBox
except ImportError:
    from tkinter import messagebox as tkMessageBox

import os.path


class Config:
    def __init__(self, path):
        self.root = Toplevel()
        self.root.title("conf.txt")

        try:

            # Use .ico file by default
            self.root.iconbitmap(FOXDOT_ICON)
            
        except TclError:

            # Use .gif if necessary
            self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file=FOXDOT_ICON_GIF))

        self.filepath = os.path.realpath(path)

        self.y_scroll = Scrollbar(self.root)
        self.y_scroll.grid(row=0, column=2, sticky='nsew')

        self.textbox = Text(self.root, width=50, yscrollcommand=self.y_scroll.set)
        self.textbox.grid(row=0, column=0, columnspan=2)

        self.exit = Button(self.root, text="Cancel", command=self.root.destroy)
        self.exit.grid(row=1, column=0, stick=N+S+E+W)

        self.save = Button(self.root, text="Save Changes", command=self.save_changes)
        self.save.grid(row=1, column=1, sticky=N+S+E+W, columnspan=2)

        self.unsaved = True

        with open(self.filepath) as f:

            self.text = f.read()

        self.textbox.insert(INSERT, self.text)
        
    def start(self):
        self.root.mainloop()

    def save_changes(self):
        text = self.textbox.get("0.0", END)
        f = open(self.filepath, "w") # writing a file
        f.write(text)
        f.close()
        self.root.destroy()
        tkMessageBox.showwarning(title="Just a heads up", message="A restart of FoxDot is required for the changes to take effect")
        return

