from Tkinter import Scrollbar, Text, Frame
from Tkinter import RIGHT, LEFT, BOTH, END, INSERT, Y, X
from Format  import *
import Queue

#!/usr/bin/python
""" Console widget that displays the true Python input """

class console:

    def __init__(self, master, font):

        self.app  = master
        self.root = master.root
        
        self.Yscroll = Scrollbar(self.root)
        self.Yscroll.grid(row=1, column=2, sticky='nsew', rowspan=2)

        # Create a bar for changing console size
        self.drag = Frame( self.root , bg="white", height=4, cursor="sb_v_double_arrow")

        # Create text bar
        self.height = 10
        self.root_h = self.height + self.app.text.height
        
        self.text = Text( self.root, padx=5, pady=5,
                          height=self.height,
                          width=10,
                          bg="Black", fg="White",
                          font=(font, 12),
                          yscrollcommand=self.Yscroll.set)

        self.Yscroll.config(command=self.text.yview)

        # Disable all key bindings EXCEPT those with function that return none
        ctrl = "Command" if SYSTEM == MAC_OS else "Control"
        self.text.bind("<Key>", lambda e: "break")
        self.text.bind("<{}-c>".format(ctrl), lambda e: None)

        # Allow for resizing
        self.mouse_down = False
        self.drag.bind("<Button-1>", self.mouseclick)
        self.drag.bind("<ButtonRelease-1>", self.mouserelease)
        self.drag.bind("<B1-Motion>", self.mousedrag)

        self.drag.grid(row=1, column=0, sticky="nsew", columnspan=2)
        self.text.grid(row=2, column=0, sticky="nsew", columnspan=2)
        
        self.queue = Queue.Queue()
        self.update()

    def __str__(self):
        """ str(s) -> string """
        return self.text.get(1.0, "end")   

    def write(self, string):
        """ Adds string to the bottom of the console """
        self.queue.put(string)
        return

    def mouseclick(self, event):
        """ Allows the user to resize the console height """
        self.mouse_down = True
        self.root.grid_propagate(False)
        return
    
    def mouserelease(self, event):
        self.mouse_down = False
        self.app.text.focus_set()
        return

    def mousedrag(self, event):
        if self.mouse_down:

            self.text.update_idletasks()

            textbox_line_h = self.app.text.dlineinfo("@0,0")

            if textbox_line_h is not None:

                self.app.text.height = int(self.app.text.winfo_height() / textbox_line_h[3])
                
            console_line_h = self.text.dlineinfo("@0,0")

            self.root_h = self.height + self.app.text.height

            if console_line_h is not None:

                widget_y = self.text.winfo_rooty()

                new_height = (self.text.winfo_height() + (widget_y - event.y_root) )

                self.height = max(2, int( new_height / console_line_h[3] ))

                self.text.config(height = self.height)
                
                self.app.text.config(height = self.root_h - self.height)

##                self.app.text.height = int((self.app.text.winfo_height()-2) / textbox_line_h[3])
##
##                print self.height, self.app.text.height

                self.text.see(END)

                return "break"
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
