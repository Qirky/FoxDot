from __future__ import absolute_import, division, print_function

try:
    import Tkinter as Tk
except ImportError:
    import tkinter as Tk

class LineNumbers(Tk.Canvas):
    def __init__(self, master, *args, **kwargs):
        Tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = master
        
        self.redraw()

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        # Draw a line

        w = self.winfo_width() - 1
        h = self.winfo_height()

        self.create_line(w, 0, w, h, fill="gray")

        i = self.textwidget.index("@0,0")
        
        while True:

            dline=self.textwidget.dlineinfo(i)

            if dline is None:
                break

            y = dline[1]
            h = dline[3]

            linenum  = int(str(i).split(".")[0])
            curr_row = int(self.textwidget.index(Tk.INSERT).split(".")[0])

            if linenum == curr_row:

                x1, y1 = 0, y
                x2, y2 = w - 2, y + h

                self.create_rectangle(x1, y1, x2, y2, fill="gray30", outline="gray30")

            self.create_text(w - 4, y, anchor="ne",
                             justify=Tk.RIGHT,
                             text=linenum,
                             font="CodeFont",
                             fill="#c9c9c9")

            i = self.textwidget.index("{}+1line".format(i))

        self.after(30, self.redraw)
