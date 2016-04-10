from Tkinter import Scrollbar, Text
from Tkinter import RIGHT, LEFT, BOTH, END, INSERT, Y, X
from formatting import DEFAULT_FONT

#!/usr/bin/python
""" Console widget that displays the true Python input """

class console:

    def __init__(self, master):

        self.Yscroll = Scrollbar(master)
        self.Yscroll.pack(side=RIGHT, fill=Y)        
        
        self.text = Text( master, padx=5, pady=5,
                            height=10,
                            bg="Black", fg="White",
                            font=(DEFAULT_FONT, 12),
                            yscrollcommand=self.Yscroll.set)

        self.Yscroll.config(command=self.text.yview)

        self.text.bind("<Key>", lambda e: "break")

        self.text.pack(fill=BOTH, expand=1)

    def __str__(self):
        """ str(s) -> string """
        return self.text.get()        

    def write(self, string):
        """ Adds string to the bottom of the console """
        self.text.insert( END, string )
        self.text.see(END)
        return

    def read(self):
        """ Returns contents of the console widget """
        return str(self)
