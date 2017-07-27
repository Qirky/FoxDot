from __future__ import absolute_import, division, print_function

try:
    from Tkinter import *
    import tkFont
except ImportError:
    from tkinter import *
    from tkinter import font as tkFont

from ..Settings import FONT

class TextPrompt:
    def __init__(self, master):
        self.value = StringVar()
        self.label = Label(master, textvariable=self.value, font="CodeFont")
        self.label.place(x=9999, y=9999)
        self.value.set("")
    def move(self, x, y):
        self.label.place(x=x, y=y)
        return
    def hide(self):
        self.label.place(x=9999, y=9999)
        return
    
