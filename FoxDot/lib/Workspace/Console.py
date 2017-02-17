from Tkinter import Scrollbar, Text
from Tkinter import RIGHT, LEFT, BOTH, END, INSERT, Y, X
import Queue

#!/usr/bin/python
""" Console widget that displays the true Python input """

class console:

    def __init__(self, master, font):

        self.root = master
        
        self.Yscroll = Scrollbar(master)
        self.Yscroll.grid(row=1, column=2, sticky='nsew')

        self.height = 7

        self.text = Text( master, padx=5, pady=5,
                          height=10,
                          width=10,
                          bg="Black", fg="White",
                          font=(font, 12),
                          yscrollcommand=self.Yscroll.set)

        self.Yscroll.config(command=self.text.yview)

        self.text.bind("<Key>", lambda e: "break")
        
        self.text.grid(row=1, column=0, sticky="nsew", columnspan=2)

        self.queue = Queue.Queue()

        self.update()

    def __str__(self):
        """ str(s) -> string """
        return self.text.get(1.0, "end")   

    def write(self, string):
        """ Adds string to the bottom of the console """
        self.queue.put(string)
        return

    def update(self):
        try:

            while True:
                string = self.queue.get_nowait()
                
                try:

                    self.text.insert( END, string )
                    self.text.see(END)

                except:
                    pass

        except Queue.Empty:

            pass

        self.root.after(50, self.update)

    def read(self):
        """ Returns contents of the console widget """
        return self.text.get(1.0, "end")

    def hide(self):
        """ Removes console from interface """
        self.text.grid_remove()
        self.Yscroll.grid_remove()
        return

    def show(self):
        self.text.grid()
        self.Yscroll.grid()
        return
