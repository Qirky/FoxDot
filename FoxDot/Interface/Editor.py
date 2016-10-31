#!/usr/bin/python

""" Tkinter interface made for Live Coding with Python syntax highlighting """  

# Tkinter Interface
from Tkinter import *
import tkFont
import tkFileDialog

# stdlib threading
from threading import Thread
from time import sleep as wait

# Custom app modules
from Format import *
from AppFunctions import *
from Console import console
from Undo import UndoStack

from ..Settings import FONT, FOXDOT_ICON
import os

# Code execution
from ..Code import execute
 
# App object

class FoxDot:

    default_font = FONT
    namespace = {}

    def __init__(self):

        # Set up master widget  

        self.root = Tk()
        self.root.title("FoxDot - Live Coding with Python and SuperCollider")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=2)
        self.root.protocol("WM_DELETE_WINDOW", self.kill )
        self.root.iconbitmap(FOXDOT_ICON)

        # Set font

        if self.default_font not in tkFont.families():

            self.default_font = 'Courier New'

        self.font = tkFont.Font(font=(self.default_font, 12), name="CodeFont")
        self.font.configure(**tkFont.nametofont("CodeFont").configure())

        # Create Y scrollbar

        self.Yscroll = Scrollbar(self.root)
        self.Yscroll.grid(row=0, column=1, sticky='nsew')

        # Create text box for code

        self.text = Text(self.root,
                         padx=5, pady=5,
                         bg=colour_map['background'],
                         fg=colour_map['plaintext'],
                         insertbackground="White",
                         font = "CodeFont",
                         yscrollcommand=self.Yscroll.set,
                         width=120, height=20)

        self.text.grid(row=0, column=0, sticky="nsew")
        self.Yscroll.config(command=self.text.yview)
        self.text.focus_set()

        # Docstring prompt label

        self.prompt = StringVar()
        self.promptlbl = Label(self.text, textvariable=self.prompt)
        self.promptlbl.place(x=9999, y=9999)
        self.last_word = ""
        self.prompt.set("")        

        # Key bindings
        
        self.text.bind("<Return>",          self.newline)
        self.text.bind("<BackSpace>",       self.delete)
        self.text.bind("<Delete>",          self.delete2)
        self.text.bind("<Tab>",             self.tab)
        self.text.bind("<Key>",             self.keypress)
        
        # Use command key on Mac (Temporary)
        
        ctrl = "Command" if SYSTEM == MAC_OS else "Control"
            
        self.text.bind("<{}-Return>".format(ctrl),          self.get_code)
        self.text.bind("<{}-a>".format(ctrl),               self.selectall)
        self.text.bind("<{}-period>".format(ctrl),          self.killall)
        self.text.bind("<{}-v>".format(ctrl),               self.paste)
        self.text.bind("<{}-bracketright>".format(ctrl),    self.indent)
        self.text.bind("<{}-bracketleft>".format(ctrl),     self.unindent)
        self.text.bind("<{}-equal>".format(ctrl),           self.zoom_in)
        self.text.bind("<{}-minus>".format(ctrl),           self.zoom_out)
        self.text.bind("<{}-z>".format(ctrl),               self.undo)
        self.text.bind("<{}-s>".format(ctrl),               self.save)
        self.text.bind("<{}-o>".format(ctrl),               self.openfile)

        # Change ctrl+h on Mac (is used to close)

        if SYSTEM == MAC_OS:
                       
            self.text.bind("<{}-k>".format(ctrl), self.help)
            self.help_key = "K"

        else:

            self.text.bind("<{}-h>".format(ctrl), self.help)
            self.help_key = "H"

        # Toggle console button keybind

        try:
            
            self.text.bind("<{}-#>".format(ctrl), self.toggle_console)
            self.toggle_key = "#"
            
        except:
            
            self.text.bind("<{}-t>".format(ctrl), self.toggle_console)
            self.toggle_key = "T" 

        # Save feature variabes

        self.saved    = False
        self.file     = None
        self.filename = None

        # Automatic brackets

        self.inbrackets = False
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

        # Create undo-stack

        self.undo_stack = UndoStack(self.text)

        # Create lable for console

        self.console = console(self.root, self.default_font)
        self.console_visible = True
        sys.stdout = self.console

        # Say Hello to the user

        print "Welcome to FoxDot! Press Ctrl+{} for help.".format(self.help_key)
        print "-----------------------------------------"

    def run(self):
        """ Starts the Tk mainloop for the master widget """
        self.root.mainloop()
        return

    """

        Key press commands
        ------------------

    """

    def keypress(self, event=None):
        """ Handles any keypress """

        # Return normally for non-string char

        if not event.char or isHex(event.char):

            self.inbrackets = False

            self.update_prompt()

            return
        
        else: # Add character to text box

            self.delete_selection()

            index = self.text.index(INSERT)
            char  = event.char

            self.text.insert(index, event.char)

            self.undo_stack.append_keystroke(index)

            self.update(event)

        return "break"

    # Undo action: Ctrl+Z
    #--------------------

    def undo(self, event=None):
        """ Ctrl+z: Remove the last character pressed """

        if len(self.undo_stack) > 0:

            self.undo_stack.pop().action()
            self.update(event)
            
        return

    # Help feature: Ctrl+H
    #---------------------

    def help(self, event=None):

        if SYSTEM == MAC_OS:
            ctrl = "Cmd"
        else:
            ctrl = "Ctrl"
            
        print "FoxDot Help:"
        print "--------------------------------------------"
        print "{}+Return  : Execute code".format(ctrl)
        print "{}+.       : Stop all sound".format(ctrl)
        print "{}+=       : Zoom in".format(ctrl)
        print "{}+-       : Zoom out".format(ctrl)
        print "{}+S       : Save your work".format(ctrl)
        print "{}+O       : Open a file".format(ctrl)
        print "{}+{}       : Toggle console window".format(ctrl, self.toggle_key)
        print "--------------------------------------------"
        print "Please visit foxdot.org for more information"
        print "--------------------------------------------"
        return "break"

    # Save the current text: Ctrl+s
    #------------------------------

    def save(self, event=None):
        """ Saves the contents of the text editor """
        text = self.text.get("0.0",END)
        if not self.saved:
            self.filename = tkFileDialog.asksaveasfilename(defaultextension=".py")
        if self.filename is not None:
            with open(self.filename, 'w') as f:
                f.write("# {}\n".format(self.filename))
                f.write("from __future__ import division\n")
                f.write("from FoxDot import *\n\n")
                f.write(text)
                f.close()
                self.saved = True
                print "Save successful!"
        return

    # Open save

    def saveAs(self,event=None):
        text = self.text.get("0.0",END)
        self.filename = tkFileDialog.asksaveasfilename(defaultextension=".py")
        if self.filename is not None:
            with open(self.filename, 'w') as f:
                f.write(text)
                f.close()
                self.saved = True
                print "Save successful!"
        return

    # Open a file: Ctrl+o
    #--------------------

    def openfile(self, event=None):
        f = tkFileDialog.askopenfile()
        if f is None:
            return
        else:
            text = f.read()
            f.close()
            self.text.delete("0.0", END)
            self.text.insert("0.0", text)
            self.update(event)
        return

    # Toggle console: Ctrl+#
    #-----------------------------
    def toggle_console(self,event=None):
        if self.console_visible:
            self.console.hide()
            self.text.config(height=self.text.cget('height')+self.console.height)
            self.console_visible = False
        else:
            self.console.show()
            self.text.config(height=self.text.cget('height')-self.console.height)
            self.console_visible = True
        return
    
    def paste(self, event=None):
        """ Ctrl-V: Pastes any text and updates the IDE """
        # Insert the data from the clipboard            
        self.text.insert(self.text.index(INSERT), self.root.clipboard_get())

        # Update the IDE colours
        self.update(event)
        
        return "break"

    # Newline
    #--------

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

    # Tab
    #----

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

    # Indent: Ctrl+]
    #---------------

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

    # Un-inden: Ctrl+[
    #-----------------

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

    # Deletion
    #---------

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
            text = self.text.get(SEL_FIRST, SEL_LAST)
            a, b = self.text.index(SEL_FIRST), self.text.index(SEL_LAST)
            self.text.delete(SEL_FIRST, SEL_LAST)
            self.undo_stack.append_delete(text, a, b)
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

    """

        Keyboard Shortcuts
        ==================

    """

    # Select all: Ctrl+a
    #-------------------

    def selectall(self, event):
        """ Ctrl-a: Select the contents of the IDE """
        self.text.tag_add(SEL, "1.0", END)
        self.text.mark_set(INSERT, "1.0")
        self.text.see(INSERT)
        return 'break'

    # Kill all: Ctrl+.
    #-----------------

    def killall(self, event):
        """ Stops all player objects """
        execute("Clock.clear()")
        return "break"

    # Zoom in: Ctrl+=
    #----------------

    def zoom_in(self, event):
        """ Ctrl+= increases text size """
        self.root.grid_propagate(False)
        font = tkFont.nametofont("CodeFont")
        size = font.actual()["size"]+2
        font.configure(size=size)
        return 'break'

    # Zoom out: Ctrl+-
    #-----------------

    def zoom_out(self, event):
        """ Ctrl+- decreases text size (minimum of 8) """
        self.root.grid_propagate(False)
        font = tkFont.nametofont("CodeFont")
        size = max(8, font.actual()["size"]-2)
        font.configure(size=size)
        return  'break'


    # Code execution: Ctrl+Return
    #----------------------------

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

    def submit(self, code_str):
        """ Runs the chunk of code through FoxDot processing and execute """
        try:
                
            execute( code_str )

        except:

            return

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

    """

        Methods that view the FoxDot namespace
        --------------------------------------

    """
        

    def update_prompt(self):
        return

    def update_prompt2(self):        

        if self.inbrackets:

            # Show prompt

            line, column = index(self.text.index(INSERT))
            text = self.text.get(index(line, 0), index(line, column))

            x = self.font.measure(text)
            y = self.font.metrics("linespace") * line

            self.promptlbl.place(x=x, y=y)

            # If cursor is in between brackets that follow a type word

            try:

                self.check_namespace()

            except:

                pass

        else:

            # Hide prompt

            self.promptlbl.place(x=9999, y=9999)

        #self.prompt.set("cheese")

    def check_namespace(self):
        """ Sets the label """

        obj = self.namespace[self.last_word]

        if obj:

            if obj.__doc__ is not None:

                self.prompt.set(obj.__doc__)

            else:

                self.promptlbl.place(x=9999, y=9999)

    """

        Methods that update the contents of the IDE
        -------------------------------------------

    """

    def update(self, event=None, row=0):
        """ Updates the the colours of the IDE """

        ### TODO - also update the rows above and below

        # Move the window to view the current line

        self.text.see(INSERT)

        # 1. Get the contents of the current line
##
##        cur = self.text.index(INSERT)
##
##        line, column = index(cur)

        # -- check current and last line if return key

        cur = self.text.index(END)
        line, column = index(cur)

        #lines = [line] + [line-1-N for N in range(row)] + [line-1] * int(isReturn(event.char))
        lines = range(line)

        for line in lines:

            start, end = index(line,0), index(line,"end")

            thisline = self.text.get(start, end)

            # 2. Remove tags at current point

            for tag_name in self.text.tag_names():

                self.text.tag_remove(tag_name, start, end)

            # 3. Re-apply tags

            for tag_name, start, end in findstyles(thisline):
                
                self.text.tag_add(tag_name, index(line, start), index(line, end))

        self.update_prompt()

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

            # Get the last word

            self.get_last_word()

            # Insert closed brackets

            self.text.insert(self.text.index(INSERT), self.all_brackets[event.char])

            # Move cursor back one place

            line, column = index(self.text.index(INSERT))

            self.text.mark_set("insert", "%d.%d" % (line, column - 1))

            # Add to the stack of "open brackets"

            self.bracket_q.append(self.all_brackets[event.char])

        # Add originally typed bracket

        self.text.insert(self.text.index(INSERT), event.char)

        self.inbrackets = True
        
        # Update any colour

        self.update(event)

        return "break"

    def get_last_word(self):

        line, column = index(self.text.index(INSERT))

        string = ""

        while True:

            char = self.text.get(index(line, column-1))

            if char.isalpha():

                string = char + string

            else:

                break

            column -= 1

            if column == 0:

                break

        self.last_word = string

    """
        Generic functions
        -----------------
        - Correct exiting
        - Tabspace (todo: customise)
        

    """

    def kill(self):
        """ Proper exit function """

        self.terminate()

        self.root.destroy()

        return
    
    def tabspace(self):
        return " " * tabsize

    def terminate(self):
        """ Called on window close. Ends Clock thread process """
        execute("Clock.stop()")
        execute("Server.quit()")
        return
