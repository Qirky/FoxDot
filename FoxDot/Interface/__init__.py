#!/usr/bin/python

""" Tkinter interface made for Live Coding with Python syntax highlighting """
import sys

# Tkinter Interface
from Tkinter import *
import tkFont

# stdlib threading
from threading import Thread
from time import sleep as wait

# Custom app modules
from formatting import *
from appfunctions import *
from consolewidget import console
 
# App object

class App:

    def __init__(self, widget_title):

        # Set up master widget  

        self.root = Tk()
        self.root.title(widget_title)
        self.root.protocol("WM_DELETE_WINDOW", self.kill )

        # Create Y scrollbar

        self.Yscroll = Scrollbar(self.root)
        self.Yscroll.pack(side=RIGHT, fill=Y)

        # Font Settings

        self.font = tkFont.Font(font=(DEFAULT_FONT, 12), name="CodeFont")
        self.font.configure(**tkFont.nametofont("CodeFont").configure())

        # Root widget container

        self.container = Frame(self.root,
                               borderwidth=1,
                               relief="sunken",
                               width=960,
                               height=400 )

        self.container.grid_propagate(False)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Create text box for code

        self.text = Text(self.container,
                         padx=5, pady=5,
                         bg = colour_map['background'],
                         fg=colour_map['plaintext'],
                         insertbackground="White",
                         font = "CodeFont",
                         yscrollcommand=self.Yscroll.set)

        self.text.grid(row=0, column=0, stick="nsew")

        self.Yscroll.config(command=self.text.yview)
        
        self.text.focus_set()

        # Key bindings
        self.text.bind("<Control-Return>",  self.get_code)
        self.text.bind("<Control-a>",       self.selectall)
        self.text.bind("<Control-.>",       self.killall)
        self.text.bind("<Control-v>",       self.paste)
        self.text.bind("<Return>",          self.newline)
        self.text.bind("<BackSpace>",       self.delete)
        self.text.bind("<Delete>",          self.delete2)
        self.text.bind("<Tab>",             self.tab)
        self.text.bind("<Control-]>",       self.indent)
        self.text.bind("<Control-[>",       self.unindent)
        self.text.bind("<Control-=>",       self.zoom_in)
        self.text.bind("<Control-minus>",   self.zoom_out)
        self.text.bind("<Key>",             self.keypress)

        # Automatic brackets

        self.separators = py_separators

        self.left_brackets  = left_b
        self.right_brackets = right_b

        self.all_brackets = dict(zip(self.left_brackets, self.right_brackets))
        self.bracket_q = []
        
        for char in self.left_brackets + self.right_brackets:
            self.text.bind(char, self.brackets)

        # Set tag names and config for specific colours

        for tier in tag_weights:

            for tag_name in tier:

                self.text.tag_config(tag_name, foreground=colour_map[tag_name])

        # Create lable for console

        self.console = console(self.root)
        sys.stdout = self.console

    def run(self):
        """ Starts the Tk mainloop for the master widget """
        self.root.mainloop()
        return

    def keypress(self, event=None):
        """ Handles any keypress """

        # Return normally for non-string char

        if not event.char or isHex(event.char):

            return
        
        else: # Add character to text box

            self.delete_selection()

            self.text.insert(self.text.index(INSERT), event.char)

            self.update(event)

        return "break"

    def update(self, event=None, row=0):
        """ Updates the the colours of the IDE """

        # Move the window to view the current line

        self.text.see(INSERT)

        # 1. Get the contents of the current line

        cur = self.text.index(INSERT)

        line, column = index(cur)

        # -- check current and last line if return key

        lines = [line] + [line-1-N for N in range(row)] + [line-1] * int(isReturn(event.char))

        for line in lines:

            start, end = index(line,0), index(line,"end")

            thisline = self.text.get(start, end)

            # 2. Remove tags at current point

            for tag_name in self.text.tag_names():

                self.text.tag_remove(tag_name, start, end)

            # 3. Re-apply tags

            for tag_name, start, end in findstyles(thisline):
                
                self.text.tag_add(tag_name, index(line, start), index(line, end))

        return "break"
                    

    def brackets(self, event):
        """ Inserts and deletes enclosing brackets automatically """

        # If a right bracket is typed and was auto added, delete it

        if self.bracket_q and event.char == self.bracket_q[-1]:

            line, column = index(self.text.index(INSERT))

            if self.text.get(index(line, column)) == self.bracket_q[-1]:
    
                self.text.delete(index(line, column))

            self.bracket_q.pop(0)

        # If a left bracket, automatically add the right

        if event.char in self.left_brackets and self.text.get(self.text.index(INSERT)) in py_whitespace + self.left_brackets + self.right_brackets:
            
            # Insert closed brackets

            self.text.insert(self.text.index(INSERT), self.all_brackets[event.char])

            # Move cursor back one place

            line, column = index(self.text.index(INSERT))

            self.text.mark_set("insert", "%d.%d" % (line, column - 1))

            # Add to the stack of "open brackets"

            self.bracket_q.append(self.all_brackets[event.char])

        # Add originally typed bracket

        self.text.insert(self.text.index(INSERT), event.char)

        # Update any colour

        self.update(event)

        return "break"

    # --- Key-binded functions

    def paste(self, event=None):
        """ Ctrl-V: Pastes any text and updates the IDE """

        # Get first row
        row1 = index(self.text.index(INSERT))[0]

        # Insert the data from the clipboard            
        self.text.insert(self.text.index(INSERT), self.root.clipboard_get())

        # Get end row
        row2 = index(self.text.index(INSERT))[0]

        n_rows = row2 - row1

        # Update the IDE colours
        self.update(event, n_rows)
        
        return "break"

    def newline(self, event):
        """ Adds whitespace to newlines where necessary """

        # Remove any highlighted text

        self.delete_selection()

        # Get the text from this line

        i, j = index(self.text.index(INSERT))
        line = self.text.get("%d.0" % i, "%d.end" % i)

        # Add newline

        self.text.insert(self.text.index(INSERT), "\n")

        pos = 0 # amount of whitespace to add

        while True:

            # Case 1. Unindented or indented but empty

            if line.strip() == "": break

            # Case 2. Open Bracket

            pos = open_bracket(line)

            if pos: break

            # Case 2. Keyword with ending ':'

            pos = function(line)

            if pos: break

            # Case 3. Indented line

            pos = indented(line)

            if pos: break

            # Any other possibilities

            pos = 0
            
            break

        # Add the necessary whitespace

        self.text.insert(self.text.index(INSERT), " " * pos )

        # Update the IDE colours

        self.update(event)

        return "break"

    def tab(self, event):
        """ Move selected text forward 4 spaces """
        try: # Move any selected lines forwards
            a, b = (index(a)[0] for a in (self.text.index(SEL_FIRST), self.text.index(SEL_LAST)))
            if a < b:
                self.indent(event)
                return "break"
            else:
                self.delete(event)
        except: 
            pass
        # Insert white space
        self.text.insert(self.text.index(INSERT), self.tabspace())
        # Update IDE
        self.update(event)
        return "break"

    def indent(self, event):
        """ Indent the current line or selected text """
        try:

            if not self.text_selected():
                a = index(self.text.index(INSERT))
                a = a[0],a[1]-1
                b = a[0],a[1]+1
                self.text.tag_add(SEL, index(*a), index(*b))

            sel_a = index(index(self.text.index(SEL_FIRST))[0],0)
            sel_b = index(index(self.text.index(SEL_LAST))[0],'end')
                
            start, end = (index(a) for a in (self.text.index(SEL_FIRST), self.text.index(SEL_LAST)))
            for row in range(start[0], end[0]+1):
                # Add intentation
                self.text.insert(index(row,0), self.tabspace())

            self.text.tag_add(SEL, sel_a, sel_b)

        except:

            pass
            
        return "break"

    def unindent(self, event):
        """ Moves the current row or selected text back by 4 spaces """
        if not self.text_selected():
            a = index(self.text.index(INSERT))
            a = a[0],a[1]-1
            b = a[0],a[1]+1
            self.text.tag_add(SEL, index(*a), index(*b))

        sel_a = index(index(self.text.index(SEL_FIRST))[0],0)
        sel_b = index(index(self.text.index(SEL_LAST))[0],'end')
            
        start, end = (index(a) for a in (self.text.index(SEL_FIRST), self.text.index(SEL_LAST)))
        for row in range(start[0], end[0]+1):
            # Unindent
            line = self.text.get(index(row,0), index(row,'end'))
            for n, char in enumerate(line[:tabsize]):
                if char != " ":
                    break
            self.text.delete(index(row,0),index(row,n+1))
            #self.text.insert(index(row,0), self.tabspace())

        self.text.tag_add(SEL, sel_a, sel_b)
        
        return "break"        

    def delete(self, event):
        """ Deletes a character or selected area """
        # If there is a selected area, delete that
        if self.delete_selection():
            return "break"
        
        # Else, work out if there is a tab to delete
        
        i, j = index(self.text.index(INSERT))

        # If we are at the start of a line, delete that

        if j == 0:
            self.update(event)
            return

        tab = index(i,j-tabsize)
        cur = index(i,j)
        char_l = self.text.get(index(i,j-1))
        char_r = self.text.get(index(i,j+1))
      
        # Check if there's a tab
        if self.text.get(tab,cur) == self.tabspace():
            self.text.delete(tab, cur)
        
        # Check if in a set of empty brackets and delete both
        elif char_l in self.left_brackets:
            for b in self.left_brackets:
                if b == self.text.get(index(i,j-1)) and self.all_brackets[b] == self.text.get(cur):
                    self.text.delete(index(i, j-1), index(i,j+1))

                elif b == self.text.get(index(i,j-1)):
                    self.text.delete(index(i, j-1))

        # Delete 1 char
        elif j > 0:

            self.text.delete(index(i, j-1))

        else:

            # Backspace as normal
            self.update(event)
            return

        # Update the IDE
        self.update(event)
        return "break"

    def delete2(self,event):
        """ Delete the next character """
        self.text.delete(self.text.index(INSERT))
        self.update(event)
        return "break"

    def delete_selection(self):
        """ If an area is selected, it is deleted and returns True """
        try:
            self.text.delete(SEL_FIRST, SEL_LAST)
            return True        
        except:
            return False

    def text_selected(self):
        """ Returns True if text is selected """
        try:
            self.text.index(SEL_FIRST)
            return True
        except:
            return False
        

    def selectall(self, event):
        """ Ctrl-a: Select the contents of the IDE """
        self.text.tag_add(SEL, "1.0", END)
        self.text.mark_set(INSERT, "1.0")
        self.text.see(INSERT)
        return 'break'

    def zoom_in(self, event):
        """ Ctrl+= increases text size """

        font = tkFont.nametofont("CodeFont")
        size = font.actual()["size"]+2
        font.configure(size=size)

        return 'break'

    def zoom_out(self, event):
        """ Ctrl+- decreases text size (minimum of 8) """

        font = tkFont.nametofont("CodeFont")
        size = max(8, font.actual()["size"]-2)
        font.configure(size=size)

        return  'break'


    # --- Placeholders

    def submit(self, code_str):
        """ Placeholder method """
        return

    def get_code(self, event):
        """ Method to highlight block of code and execute """

        # Get start and end of the buffer
        start, end = "1.0", self.text.index(END)
        lastline   = int(end.split('.')[0]) + 1

        # Indicies of block to execute
        block = [0,0]        
        
        # 1. Get position of cursor
        cursor = self.text.index(INSERT)
        cur_x, cur_y   = (int(a) for a in cursor.split('.'))
        
        # 2. Go through line by line (back) and see what it's value is
        
        for line in range(cur_x, 0, -1):
            if not self.text.get("%d.0" % line, "%d.end" % line).strip():
                break

        block[0] = line

        # 3. Iterate forwards until we get two \n\n or index==END
        for line in range(cur_x, lastline):
            if not self.text.get("%d.0" % line, "%d.end" % line).strip():
                break

        block[1] = line

        # Now we have the lines of code!

        a, b = ("%d.0" % n for n in block)

        # Highlight text to execute

        self.highlight(a, b)

        # Execute the python code
        
        self.submit( self.text.get( a , b ) )

        # Unhighlight the line of text

        Thread(target=self.unhighlight).start()

        return "break"

    def highlight(self, start, end):
        """ Highlights block of code on execution """

        # Label block (start and end are the lines before and after the code itself)

        a, b = (int(n.split('.')[0]) for n in (start, end))

        if a == 1: a = 0

        for line in range(a + 1, b):
            start = "%d.0" % line
            end   = "%d.end" % line
            self.text.tag_add("code", start, end)

        # Highlight
        
        self.text.tag_config("code", background="Red", foreground="White")

        return

    def unhighlight(self):
        """ Creates thread to wait 0.2 seconds before removing any highlights from the text """

        # Hold highlight
        
        wait(0.2)

        # Remove labels

        self.text.tag_delete("code")

        return

    def kill(self):
        """ Proper exit function """

        self.terminate()

        self.root.destroy()

        return
    
    def tabspace(self):
        return " " * tabsize

    def killall(self, event):
        """ Ctrl+. function to be defined by the user """
        return

    def terminate(self):
        """ To be overridden by user to be called on window close """
        return
