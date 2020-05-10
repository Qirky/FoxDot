from __future__ import absolute_import, division, print_function

from .tkimport import Text, SEL, END, SEL_FIRST, SEL_LAST, INSERT

from .Format import *

try:
    import Queue
except ImportError:
    import queue as Queue

background = colour_map['background']

class ThreadedText(Text):
    def __init__(self, master, **options):
        Text.__init__(self, master, **options)
        self.root = master
        self.config(
            highlightbackground=background,
            selectbackground="Dodger Blue",
            selectforeground="White",
            highlightthickness=0
        )
        self.height = options.get("height", 20)
        self.queue = Queue.Queue()
        self.lines = 0 # number of lines in the text
        self.modifying = False
        self.update()

    def on_resize(self, event):
        line_h = self.dlineinfo("@0,0")
        if line_h is not None:
            self.height = int((self.winfo_height()-2) / line_h[3])
        return

    def get_num_lines(self):
        self.lines = len(self.get("1.0", END).split("\n"))
        return self.lines
    
    def update(self):
        """ Recursively called method that monitors as
            queue of Tkinter tasks.
        """
        try:
            
            while True:

                task, args, kwargs = self.queue.get_nowait()

                task(*args, **kwargs)
                
                self.update_idletasks()

        # Break when the queue is empty
        except Queue.Empty:

            pass

        except Exception as e:

            print(e)

        # Recursive call
        self.after(10, self.update)
        return

    def has_selection(self):
        """ Returns True if the selection tag is present in the text box """
        return bool(self.tag_ranges(SEL))

    def remove_selection(self):
        """ Removes selection from the entire document """
        self.tag_remove(SEL, "1.0", END)
        return 

    def is_selected(self, index):
        """ Returns True if the character at index has the SEL tag """
        return self.index(index) in self.char_range(SEL_FIRST, SEL_LAST) if self.has_selection() else False

    def row_col(self, index):
        return tuple([int(x) for x in self.index(index).split(".")])

    def is_after(self, index1, index2):
        """ Returns True if index1 is after index2, returns True if they are equal """
        a_row, a_col = self.row_col(index1)
        b_row, b_col = self.row_col(index2)
        return (a_row > b_row) or (a_row == b_row and a_col >= b_col)

    def is_before(self, index1, index2):
        """ Returns True if index1 is after index2, returns True if they are equal """
        return not self.is_after(index1, index2)

    def char_range(self, index1, index2):
        """ Returns a list of indices between two Tk indices"""
        if self.is_after(index1, index2):
            
            index1, index2 = index2, index1
            reverse = True

        else:
            
            reverse = False

        a_row, a_col = self.row_col(index1)
        b_row, b_col = self.row_col(index2)

        data = []
        
        for row in range(a_row, b_row + 1,):
            if row == a_row:
                x1_col = a_col
            else:
                x1_col = 0
            if row == b_row:
                x2_col = b_col
            else:
                _, x2_col = self.row_col(self.index("{}.{}".format(row, END)))
            
            for col in range(x1_col, x2_col):
                
                data.append( "{}.{}".format(row, col) )

        if reverse:

            data = list(reversed(data))

        return data

    def get_visible_range(self):
        """ Returns a tuple of integers for the first and last row visible in the editor """
        a = self.index("@0,0")
        b = self.index("@0,%d" % self.winfo_height())
        return tuple(int(s.split(".")[0]) for s in (a, b)) 
