from __future__ import absolute_import, division, print_function

try:
    from Tkinter import *
except ImportError:
    from tkinter import *
    
from .Format  import *
from .AppFunctions import stdout
import math
import random

try:
    import Queue
except ImportError:
    import queue as Queue

#!/usr/bin/python
""" Console widget that displays the true Python input """

class console:

    def __init__(self, master, font):

        self.app  = master
        self.root = master.root
        
        self.y_scroll = Scrollbar(self.root)
        self.y_scroll.grid(row=2, column=2, sticky='nsew', rowspan=2)
        self.scrollable = False

        # Create a bar for changing console size

        self.drag = Frame( self.root , bg="white", height=2, cursor="sb_v_double_arrow")

        # Create canvas

        self.height = 10
        self.max_offset = 0
        self.root_h = self.height + self.app.text.height

        self.canvas = Canvas(self.root,
                             bg="black",
                             bd=0,
                             height=300,
                             yscrollincrement=1,
                             highlightthickness=0)

        self.canvas.bind("<Button-1>",          self.canvas_mouseclick)
        self.canvas.bind("<ButtonRelease-1>",   self.canvas_mouserelease)
        self.canvas.bind("<B1-Motion>",         self.canvas_mousedrag)
        self.canvas.bind("<MouseWheel>",        self.on_scroll)
        self.canvas.bind("<{}-c>".format("Command" if SYSTEM == MAC_OS else "Control"),   self.edit_copy)

        self.padx = 5
        self.pady = 5
        
        self.text_y = 0

        self.text_height = 0
        self.canvas_height = 0

        # Draw logo

        self.draw_logo()

        # Create text

        self.text = self.canvas.create_text((self.padx, self.pady),
                                            anchor=NW,
                                            fill="white",
                                            font=(font,12) )

        self.text_cursor = None

        self.y_scroll.config(command=self.scroll_text)

        # Allow for resizing
        self.mouse_down = False
        self.drag.bind("<Button-1>",        self.drag_mouseclick)        
        self.drag.bind("<ButtonRelease-1>", self.drag_mouserelease)
        self.drag.bind("<B1-Motion>",       self.drag_mousedrag)

        self.drag.grid(row=1, column=0, stick="nsew", columnspan=3)
        self.canvas.grid(row=2, column=0, sticky="nsew", columnspan=2)
    
        self.queue = Queue.Queue()
        self.update()

    def __str__(self):
        """ str(s) -> string """
        return self.text.get(1.0, "end")

    def clear(self):
        """ Clears the console """
        self.canvas.dchars(self.text, 0, "end")
        return

    def config(self, *args, **kwargs):
        self.canvas.config(*args, **kwargs)
        return

    def flush(self):
        return

    def write(self, string):
        """ Adds string to the bottom of the console """
        self.queue.put(string)
        return

    def drag_mouseclick(self, event):
        """ Allows the user to resize the console height """
        self.mouse_down = True
        self.root.grid_propagate(False)
        return
    
    def drag_mouserelease(self, event):
        self.mouse_down = False
        self.app.text.focus_set()
        return

    def drag_mousedrag(self, event):
        if self.mouse_down:

            textbox_line_h = self.app.text.dlineinfo("@0,0")

            if textbox_line_h is not None:

                self.app.text.height = int(self.app.text.winfo_height() / textbox_line_h[3])
                
            self.root_h = self.height + self.app.text.height

            widget_y = self.canvas.winfo_rooty()

            new_height = (self.canvas.winfo_height() + (widget_y - event.y_root) )

            self.height, old_height = new_height, self.height

            self.canvas.config(height = max(self.height, 50))

            return "break"

    def update(self):
        try:

            while True:

                # Add last "print" to the console text

                string = self.queue.get_nowait()

                self.canvas.itemconfig(self.text, width=self.canvas.winfo_width())

                self.canvas.insert( self.text, "end", string )

                # Get the text bounding box
                
                bbox = self.canvas.bbox(self.text)

                # Text box height

                self.text_height = bbox[3] - bbox[1]

                # Canvas height

                self.canvas_height = self.canvas.winfo_height()

                # Only allow scrolling when the text is larger than the canvas

                if self.text_height > self.canvas_height:

                    self.scrollable = True

                    # The text should only move so that the end is at the bottom of the canvas

                    self.text_y = self.max_offset = self.canvas_height - self.text_height

                    self.canvas.coords(self.text, (self.padx, self.text_y))

                else:

                    self.scrollable = False

                self.update_scrollbar()

        except Queue.Empty:

            pass

        self.root.after(50, self.update)

    def read(self):
        """ Returns contents of the console widget """
        return self.canvas.itemcget(self.text, "text")

    def hide(self):
        """ Removes console from interface """
        self.canvas.grid_remove()
        self.y_scroll.grid_remove()
        return

    def show(self):
        self.canvas.grid()
        self.y_scroll.grid()
        return

    def canvas_mouseclick(self, event):
        """ Forces the text to align itself and gives focus to the console """
        self.canvas.insert( self.text, "end", "" )
        self.canvas.focus_set()
        self.canvas.focus(self.text)

        # Remove current selection
        self.canvas.select_clear()

        # Calculate current mouse pos
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasx(event.y)
        
        self.text_cursor = "@%d,%d" % (x, y)
        
        return

    def canvas_mousedrag(self, event):
        """ Changes selection """
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasx(event.y)
        
        xy = "@%d,%d" % (x, y)
        
        self.canvas.select_from(self.text, self.text_cursor)
        self.canvas.select_to(self.text, xy)
        return

    def canvas_mouserelease(self, event):
        self.text_cursor = None
        return

    def edit_copy(self, event):
        if self.canvas.select_item() == self.text:
            self.root.clipboard_clear()
            a = self.canvas.index(self.text, SEL_FIRST)
            b = self.canvas.index(self.text, SEL_LAST) + 1
            self.root.clipboard_append(self.canvas.itemcget(self.text, "text")[a:b])
        return "break"

    def scroll_text(self, *args):
        # Moves the text by an amount (pressing the arrow buttons)
        if args[0] == "scroll":
            self.move_text(int(args[1])*-1000)
        # Dragging the scroll bar
        elif args[0] == "moveto":
            new_y = float(args[1])
            a, b = self.update_scrollbar(new_y)
            size = b - a
            self.text_y = (new_y / (1 - size)) * self.max_offset + self.pady
            self.canvas.coords(self.text, (self.padx, self.text_y))
        return

    def move_text(self, delta):
        """ Moves the text up (negative) or down (positive) """
    
        if SYSTEM != MAC_OS:

            delta /= 100
        
        x, y = self.canvas.coords(self.text)

        self.text_y = max(min(self.pady, y + delta), self.max_offset)

        self.canvas.coords(self.text, (x, self.text_y))

        self.update_scrollbar()

        return
        
    def on_scroll(self, event):
        if self.scrollable: self.move_text(event.delta)            
        return "break"

    def get_scrollbar_size(self):
        return float(self.canvas_height) / self.text_height

    def update_scrollbar(self, point=None):
        """ point should be a value between 0 and 1.0 """
        if not self.scrollable:
            a, b = 0.0, 1.0
        elif self.text_height != 0 and self.max_offset != 0:
            size = self.get_scrollbar_size()
            if point is not None:
                a = point
            else:
                a = (float(self.text_y) / self.max_offset) * (1-size)
            b = a + size        
        self.y_scroll.set(a, b)
        return a, b

    def draw_arrow(self, start_x, start_y, width, colour,  direction, degree=45,):
        """ Works out the line to draw at 45 degrees, returns the x and y of the end
            of the line. Direction should be a string, "up" or "down" """

        # Work out the height

        height = int(math.tan(math.radians(degree)) * (width / 2.0))

        # Draw line up

        end_x = start_x + (width / 2.0)
        end_y = (start_y - height) if direction == "up" else (start_y + height)

        self.canvas.create_line((start_x, start_y, end_x, end_y), fill=colour, width=3)

        # Draw line down

        start_x, start_y = end_x, end_y

        end_x = start_x + (width / 2.0)
        end_y = (start_y + height) if direction == "up" else (start_y - height)

        self.canvas.create_line((start_x, start_y, end_x, end_y), fill=colour, width=3)

        # Return the end x, y

        return end_x, end_y

    def draw_logo(self):
        """ Draws the red and green lines in the bg of the console.
         Future versions will have randomly created lines & possibly
         animated.
        """
        # All lines are 45 degress up then down
        grn_widths = [
            random.randint(400, 600), # Large
            random.randint(150, 350), # Medium
            random.randint(25, 100),    # Small
            ]

        # Shuffle the widths and use a mirrored version for red
        random.shuffle(grn_widths)
        
        red_widths = reversed(grn_widths)

        start_x = random.choice([50,100,150,200])
        start_y = random.choice([50,100])
        step    = random.choice([10,20,25])

        # Draw Red line
        x, y = start_x, start_y
        for w in red_widths:
            x, y = self.draw_arrow(x, y, w, '#571d0c', "down")
            x += step

        # Draw Green line
        # Define start point
        x, y = start_x, start_y + 100
        for w in grn_widths:
            x, y = self.draw_arrow(x, y, w, '#1d5335', "up")
            x += step
        return
