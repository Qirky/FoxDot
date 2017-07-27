# -*- coding: utf-8 -*-
#!/usr/bin/python

from __future__ import absolute_import, division, print_function

""" Tkinter interface made for Live Coding with Python syntax highlighting """  

# Tkinter Interface

try:
    from Tkinter import *
    import ttk
    import tkFont
    import tkFileDialog
    import tkMessageBox
except ImportError:
    from tkinter import *
    from tkinter import ttk
    from tkinter import font as tkFont
    from tkinter import filedialog as tkFileDialog
    from tkinter import messagebox as tkMessageBox

# Custom app modules
from .Format import *
from .AppFunctions import *
from .Console import console
from .Prompt import TextPrompt
from .BracketHandler import BracketHandler
from .TextBox import ThreadedText
from .LineNumbers import LineNumbers
from .MenuBar import MenuBar

import webbrowser
import os
import re

# Code execution
from ..Code import execute
from ..Settings import FONT, FOXDOT_ICON, SC3_PLUGINS, FOXDOT_CONFIG_FILE

# App object

class workspace:

    default_font = FONT
    namespace = {}

    def __init__(self, CodeClass):

        # Configure FoxDot's namespace to include the editor

        CodeClass.namespace['FoxDot'] = self
        CodeClass.namespace['Player'].widget = self
        #CodeClass.namespace['Ghost'].widget = self

        # Used for docstring prompt
        
        self.namespace = CodeClass.namespace

        # Set up master widget  

        self.root = Tk(className='FoxDot')
        self.root.title("FoxDot - Live Coding with Python and SuperCollider")
        self.root.rowconfigure(0, weight=1) # Text box
        self.root.rowconfigure(1, weight=0) # Separator
        self.root.rowconfigure(2, weight=0) # Console
        self.root.grid_columnconfigure(0, weight=0) # line numbers
        self.root.grid_columnconfigure(1, weight=1) # Text boxes
        self.root.protocol("WM_DELETE_WINDOW", self.kill )

        # --- Set icon
        
        try:

            # Use .ico file by default
            self.root.iconbitmap(FOXDOT_ICON)
            
        except:

            # Use .gif if necessary
            self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file=FOXDOT_ICON))

        # --- Setup font

        if self.default_font not in tkFont.families():

            if SYSTEM == WINDOWS:

                self.default_font = "Consolas"

            elif SYSTEM == MAC_OS:

                self.default_font = "Monaco"

            else:

                self.default_font = "Courier New"
        
        self.font = tkFont.Font(font=(self.default_font, 12), name="CodeFont")
        self.font.configure(family=self.default_font)

        # --- start create menu

        self.menu = MenuBar(self, visible = True)
       
        # Create y-axis scrollbar

        self.y_scroll = Scrollbar(self.root)
        self.y_scroll.grid(row=0, column=2, sticky='nsew')

        # Create text box for code

        self.text = ThreadedText(self.root,
                                 padx=5, pady=5,
                                 bg=colour_map['background'],
                                 fg=colour_map['plaintext'],
                                 insertbackground="White",
                                 font = "CodeFont",
                                 yscrollcommand=self.y_scroll.set,
                                 width=100,
                                 height=20,
                                 bd=0,
                                 undo=True, autoseparators=True,
                                 maxundo=50 )

        self.text.grid(row=0, column=1, sticky="nsew")
        self.y_scroll.config(command=self.text.yview)
        self.text.focus_set()

        # Create box for line numbers

        self.linenumbers = LineNumbers(self.text, width=25,
                                       bg=colour_map['background'],
                                       bd=0, highlightthickness=0 )
        
        self.linenumbers.grid(row=0, column=0, sticky='nsew')
        

        # Docstring prompt label

        self.prompt = TextPrompt(self.text)        

        # Key bindings (Use command key on Mac)

        ctrl = "Command" if SYSTEM == MAC_OS else "Control"
        
        self.text.bind("<Return>",          self.newline)
        self.text.bind("<BackSpace>",       self.backspace)
        self.text.bind("<Delete>",          self.delete)
        self.text.bind("<Tab>",             self.tab)
        self.text.bind("<Key>",             self.keypress)

        self.text.bind("<{}-BackSpace>".format(ctrl),       self.delete_word)
        self.text.bind("<{}-Delete>".format(ctrl),          self.delete_next_word)
            
        self.text.bind("<{}-Return>".format(ctrl),          self.exec_block)
        self.text.bind("<Alt-Return>",                      self.exec_line)
        
        self.text.bind("<Alt_L>",                           lambda event: "break")

        self.text.bind("<{}-a>".format(ctrl),               self.selectall)

        self.text.bind("<{}-period>".format(ctrl),          self.killall)
        self.text.bind("<Alt-period>".format(ctrl),         self.releaseNodes)

        self.text.bind("<{}-c>".format(ctrl),               self.edit_copy)
        self.text.bind("<{}-x>".format(ctrl),               self.edit_cut)
        self.text.bind("<{}-v>".format(ctrl),               self.edit_paste)

        self.text.bind("<{}-bracketright>".format(ctrl),    self.indent)
        self.text.bind("<{}-bracketleft>".format(ctrl),     self.unindent)

        self.text.bind("<{}-equal>".format(ctrl),           self.zoom_in)
        self.text.bind("<{}-minus>".format(ctrl),           self.zoom_out)

        self.text.bind("<{}-z>".format(ctrl),               self.undo)
        self.text.bind("<{}-y>".format(ctrl),               self.redo)

        self.text.bind("<{}-s>".format(ctrl),               self.save)
        self.text.bind("<{}-o>".format(ctrl),               self.openfile)
        self.text.bind("<{}-n>".format(ctrl),               self.newfile)

        self.text.bind("<{}-m>".format(ctrl),               self.toggle_menu)

        self.text.bind("<{}-l>".format(ctrl),               self.insert_lambda_symbol)

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

        # --- define bracket behaviour

        self.bracketHandler = BracketHandler(self)

        # Set tag names and config for specific colours

        for tier in tag_weights:

            for tag_name in tier:

                self.text.tag_config(tag_name, foreground=colour_map[tag_name])

        # --- Create console

        self.console = console(self, self.default_font)
        self.console_visible = True
        sys.stdout = self.console
        self.text.bind("<Button-1>", lambda e: self.console.canvas.select_clear())

        # Store original location of cursor
        self.origin = "origin"
        self.text.mark_set(self.origin, INSERT)
        self.text.mark_gravity(self.origin, LEFT)

        # Say Hello to the user

        hello = "Welcome to FoxDot! Press Ctrl+{} for help.".format(self.help_key)

        print(hello)
        print("-" * len(hello))

    def run(self):
        """ Starts the Tk mainloop for the master widget """
        try:
            self.root.mainloop()
        except (KeyboardInterrupt, SystemExit):
            execute("Clock.stop()")
            execute("Server.quit()")
        return

    def read(self):
        return self.text.get("1.0", END)

    """

        Key press commands
        ------------------

    """

    def keypress(self, event=None):
        """ Handles any keypress """

        # For non string characters, return normally

        self.text.tag_delete("tag_open_brackets")

        if not event.char or isHex(event.char):

            self.inbrackets = False

            self.update_prompt()

            return

        # Add character to text box
        
        else:

            self.delete_selection()

            index = self.text.index(INSERT)

            self.text.insert(index, event.char)

            self.text.edit_separator()

            self.update(event)

        return "break"

    """

        Getting blocks / lines

    """

    def exec_line(self, event=None, insert=INSERT):
        """ Highlights a single line and executes """
        line, column = index(self.text.index(insert))
        
        a, b = "%d.0" % line, "%d.end" % line

        self.highlight(a, b, "red")

        try:

            execute( self.text.get(a, b) )
            execute.update_line_numbers(self.text, a, b)

        except:

            pass

        self.root.after(200, self.unhighlight)

        return "break"

    def exec_block(self, event=None, insert=INSERT):
        """ Method to highlight block of code and execute """
        try:

            # Evaluate selection

            a = index(self.text.index(SEL_FIRST))[0]
            b = index(self.text.index(SEL_LAST))[0] + 1

        except TclError:

            # Get start and end of the buffer
            start, end = "1.0", self.text.index(END)
            lastline   = int(end.split('.')[0]) + 1

            # Indicies of block to execute
            block = [0,0]        
            
            # 1. Get position of cursor
            cur_x, cur_y = index(self.text.index(insert))
            
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

            a, b = block
        
        if a == b: b += 1

        for line in range(a, b):
            start = "%d.0" % line
            end   = "%d.end" % line

            # Highlight text only to last character, not whole line

            self.highlight(start, end)

        # Convert line numbers to Tkinter indices

        a, b = ("%d.0" % n for n in (a, b))

        # Execute the python code

        try:

            execute( self.text.get( a , b ) )
            execute.update_line_numbers(self.text, a, b)

        except:

            pass

        # Unhighlight the line of text

        self.root.after(200, self.unhighlight)

        return "break"

    # Scheduling tasks
    # ----------------
    def addTask(self, target, args=(), kwargs={}):
        self.text.queue.put((target, args, kwargs))
        return


    def insert_lambda_symbol(self, event):
        self.text.insert(INSERT, u"\u03BB")
        self.update(event)
        return

    # Undo action: Ctrl+Z
    #--------------------

    def undo(self, event=None):
        try:
            self.text.edit_undo()
            self.update_all()
        except:
            pass
             
        return "break"

    def redo(self, event=None):
        try:
            self.text.edit_redo()
            self.update_all()
        except:
            pass
        return "break"

    # Help feature: Ctrl+H
    #---------------------

    def help(self, event=None):

        if SYSTEM == MAC_OS:
            ctrl = "Cmd"
        else:
            ctrl = "Ctrl"
            
        print("FoxDot Help:")
        print("--------------------------------------------")
        print("{}+Return  : Execute code".format(ctrl))
        print("{}+.       : Stop all sound".format(ctrl))
        print("{}+=       : Increase font size".format(ctrl))
        print("{}+-       : Decrease font size".format(ctrl))
        print("{}+S       : Save your work".format(ctrl))
        print("{}+O       : Open a file".format(ctrl))
        print("{}+M       : Toggle the menu".format(ctrl))
        print("{}+{}       : Toggle console window".format(ctrl, self.toggle_key))
        print("--------------------------------------------")
        print("Please visit foxdot.org for more information")
        print("--------------------------------------------")
        return "break"

    # Save the current text: Ctrl+s
    #------------------------------

    def save(self, event=None):
        """ Saves the contents of the text editor """
        text = self.text.get("0.0",END)
        if not self.saved:
            self.filename = tkFileDialog.asksaveasfilename(filetypes=[("Python files", ".py"),("FoxDot files", ".fox")],
                                                           defaultextension=".py")
        if self.filename:
            with open(self.filename, 'w') as f:
                f.write(text)
                f.close()
                self.saved = True
                print("Saved '{}'".format(self.filename))
        return bool(self.filename)

    # Open save

    def saveAs(self,event=None):
        text = self.text.get("0.0",END)
        self.filename = tkFileDialog.asksaveasfilename(filetypes=[("Python files", ".py"),("FoxDot files", ".fox")],
                                                       defaultextension=".py")
        if self.filename is not None:
            with open(self.filename, 'w') as f:
                f.write(text)
                f.close()
                self.saved = True
                print("Save successful!")
        return bool(self.filename)

    # Open a file: Ctrl+o
    #--------------------

    def openfile(self, event=None):
        f = tkFileDialog.askopenfile()
        if f is not None:
            text = f.read()
            f.close()
            self.set_all(text)
        return "break"

    def newfile(self, event=None):
        ''' Clears the document and asks if the user wants to save '''
        answer = tkMessageBox.askyesnocancel("", "Save your work before creating a new document?")
        if answer is not None:
            if answer is True:
                if not self.save():
                    return "break"
            self.saved = False
            self.filename = ''
            self.set_all("")
        return "break"

    def export_console(self):
        fn = tkFileDialog.asksaveasfilename(filetypes=[("Plain Text File", ".txt")],
                                            defaultextension='.txt')
        with open(fn, 'w') as f:
            f.write(self.console.read())
        return

    def open_config_file(self):
        from ConfigFile import Config
        Config(FOXDOT_CONFIG_FILE).start()
        return

    def open_samples_folder(self):
        import subprocess
        
        if SYSTEM == WINDOWS:
            cmd = 'explorer'
        elif SYSTEM == MAC_OS:
            cmd = 'open'
        else:
            cmd = 'xdg-open'
        try:
            subprocess.Popen([cmd, FOXDOT_SND])
        except OSError as e:
            print(e)
            print("Hmm... Looks like we couldn't open the directory but you can find the samples in {}".format(FOXDOT_SND))
            
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

    def toggle_menu(self, event=None):
        self.menu.toggle()
        return "break"

    def toggle_sc3_plugins(self, event=None):
        """ Allows you to change the SC3 plugins variable from the editor. Restart
            of the editor is required. """
        with open(FOXDOT_CONFIG_FILE, "r") as f:
            lines = f.readlines()
        with open(FOXDOT_CONFIG_FILE, "w") as f:
            for line in lines:
                if "SC3_PLUGINS" in line:
                    f.write( "SC3_PLUGINS={}\n".format(not bool(SC3_PLUGINS)) )
                else:
                    f.write(line)
        # Pop-up to tell the user a restart is required
        tkMessageBox.showwarning(title="Just a heads up", message="Restart of FoxDot is required for the changes to take effect")
        return "break"
    
    def edit_paste(self, event=None):
        """ Pastes any text and updates the IDE """
        self.text.event_generate("<<Paste>>")
        self.update_all()
        return "break"

    def edit_cut(self, event=None):
        self.text.event_generate("<<Cut>>")
        return "break"

    def edit_copy(self, event=None):
        self.text.event_generate("<<Copy>>")
        return "break"

    # Newline
    #--------

    def newline(self, event=None, insert=INSERT):
        """ Adds whitespace to newlines where necessary """

        # Remove any highlighted text

        self.delete_selection()

        self.text.tag_delete("tag_open_brackets")

        # Get the text from this line

        i, j = index(self.text.index(insert))
        line = self.text.get("%d.0" % i, "%d.end" % i)

        # Add newline

        self.text.insert(index(i, j), "\n")

        # Update player line numbers

        execute.update_line_numbers(self.text)

        pos = 0 # amount of whitespace to add

        while True:

            # Case 1. Unindented or indented but empty

            if line.strip() == "": break

            # Case 2. Open Bracket

            # pos = open_bracket(line)

            # if pos: break

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

        self.text.insert(index(i+1,0), " " * pos )

        # Update the IDE colours

        self.update(event)
        
        return "break"

    # Tab
    #----

    def tab(self, event=None, insert=INSERT):
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

        line, column = index(self.text.index(insert))
        
        self.text.insert(index(line, column), self.tabspace())

        # Update IDE

        self.update(event)
            
        return "break"

    # Indent: Ctrl+]
    #---------------

    def indent(self, event=None, insert=INSERT):
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

            if n > 0:
                
                self.text.delete(index(row,0),index(row,n+1))

        self.text.tag_add(SEL, sel_a, sel_b)    
        return "break"

    # Deletion
    #---------

    def backspace(self, event=None, insert=INSERT):
        """ Deletes a character or selected area """
        # If there is a selected area, delete that

        if self.delete_selection():

            # Update player line numbers

            execute.update_line_numbers(self.text)

            return "break"

        # Handle delete in brackets

        if self.bracketHandler.delete():

            return "break"
    
        # Else, work out if there is a tab to delete
        
        line, column = index(self.text.index(insert))

        # If we are at the start of a line, delete that

        if column == 0:

            self.update(event)

            # Update player line numbers

            execute.update_line_numbers(self.text, start="%d.0" % (line-1), remove=int(line!=1))

            self.text.delete(index(line-1, END), insert)

        else:

            tab = index(line, column-tabsize)
        
            # Check if there's a tab
            
            if self.text.get(tab, insert) == self.tabspace():

                self.text.delete(tab, insert)

            else:

                self.text.delete(index(line, column-1), insert)
                
        # Update the IDE
        self.update(event)

        return "break"

    def delete(self, event=None, insert=INSERT):
        """ Delete the next character """

        if not self.delete_selection():

            self.text.delete(self.text.index(insert))
            
        self.update(event)

        execute.update_line_numbers(self.text)

        return "break"

    def look(self, direction=-1):
        """ Finds the start of the next / previous word """

        num_words = abs(direction)
        direction = 1 if direction > 0 else -1
        
        end = self.text.index(INSERT)

        row, col = index(end)

        # If the col is 0, set the index to the end of the previous row (unless first row)

        if direction == -1:

            if row == 1 and col == 0:

                return "1.0", "1.0"

            elif row > 1 and col == 0:

                row, col = index(self.text.index("%d.end" % (row + direction)))

                end = index(row, col)                

        # If the left char is whitespace, delete that AND the next word

        start = None

        if direction == -1:

            not_at_end = lambda x: x > 0

        else:

            _, end_point = index(self.text.index("%d.end" % row))

            not_at_end = lambda x: x < end_point

        while not_at_end(col):

            start = index(row, col + direction)

            char = self.text.get(start)

            # if the character is a space, delete that
            if char in " \t":

                start = index(row, col)
                break

            elif char in ".,()[]{}=\"'":

                start = index(row, col + (1 if direction == -1 else 0))
                break

            col = col + direction

        # return the "larger index" second

        if index(start) > index(end):

            start, end = end, start

        return start, end

    def delete_word(self, event):
        """ Deletes the preceeding text """

        if not self.delete_selection():

            start, end = self.look(-1)

            self.text.delete(start, end)

        self.update(event)

        execute.update_line_numbers(self.text)

        return

    def delete_next_word(self, event):
        """ Deletes the following word """

        if not self.delete_selection():

            start, end = self.look(1)

            self.text.delete(start, end)

        self.update(event)

        execute.update_line_numbers(self.text)

        return
        

    def delete_selection(self):
        """ If an area is selected, it is deleted and returns True """
        try:
            text = self.text.get(SEL_FIRST, SEL_LAST)
            a, b = self.text.index(SEL_FIRST), self.text.index(SEL_LAST)
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

    """

        Keyboard Shortcuts
        ==================

    """

    # Select all: Ctrl+a
    #-------------------

    def selectall(self, event=None):
        """ Select the contents of the editor """
        self.text.tag_add(SEL, "1.0", END)
        self.text.mark_set(INSERT, "1.0")
        self.text.see(INSERT)
        return 'break'

    # Kill all: Ctrl+.
    #-----------------

    def killall(self, event=None):
        """ Stops all player objects """
        execute("Clock.clear()")
        return "break"

    # Zoom in: Ctrl+=
    #----------------

    def zoom_in(self, event=None):
        """ Ctrl+= increases text size """
        self.root.grid_propagate(False)
        font = tkFont.nametofont("CodeFont")
        size = font.actual()["size"]+2
        font.configure(size=size)
        # Increase size of line number
        self.linenumbers.config(width=self.linenumbers.winfo_width() + 3)
        return 'break'

    # Zoom out: Ctrl+-
    #-----------------

    def zoom_out(self, event=None):
        """ Ctrl+- decreases text size (minimum of 8) """
        self.root.grid_propagate(False)
        font = tkFont.nametofont("CodeFont")
        size = font.actual()["size"]-2
        if size >= 8:
            font.configure(size=size)
            self.linenumbers.config(width=self.linenumbers.winfo_width() - 3)
        return  'break'
    

    def submit(self, code_str):
        """ Runs the chunk of code through FoxDot processing and execute """
        try:
                
            execute( code_str )

        except Exception as e:

            print(e)

    def highlight(self, start, end, colour="Red"):
        """ Highlights an area of text """

        # Label block (start and end are the lines before and after the code itself)

        self.text.tag_add("code", start, end)

        # Highlight
        
        self.text.tag_config("code", background=colour, foreground="White")

        return

    def unhighlight(self):
        """ Creates thread to wait 0.2 seconds before removing any highlights from the text """

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

            self.prompt.move(x, y)

            # If cursor is in between brackets that follow a type word

            try:

                self.check_namespace()

            except:

                pass

        else:

            # Hide prompt

            self.prompt.hide()

    def check_namespace(self):
        """ Sets the label """

        obj = self.namespace[self.last_word]

        if obj:

            if obj.__doc__ is not None:

                self.prompt.value.set(obj.__doc__)

            else:

                self.prompt.hide()

    """

        Methods that update the contents of the IDE
        -------------------------------------------

    """

    def update(self, event=None, insert=INSERT):
        """ Updates the the colours of the IDE """

        # Move the window to view the current line

        self.text.see(INSERT)

        # 1. Get the contents of the current line

        cur = self.text.index(insert)
        line, column = index(cur)

        self.colour_line(line)

        self.update_prompt()

        return "break"

    def update_all(self):
        """ Updates every line in the IDE """

        row, col = index(self.text.index(END))
        lines = row + 1

        for line in range(lines):

            self.colour_line(line)

        return

    def colour_line(self, line):
        """ Checks a line for any tags that match regex and updates IDE colours """

        start, end = index(line,0), index(line,"end")

        thisline = self.text.get(start, end)

        try:

            # Remove tags at current point

            for tag_name in self.text.tag_names():

                self.text.tag_remove(tag_name, start, end)

            # Re-apply tags

            for tag_name, start, end in findstyles(thisline):
                
                self.text.tag_add(tag_name, index(line, start), index(line, end))

        except Exception as e:

            print(e)

        return                    

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

    def releaseNodes(self, event=None):
        execute("Server.freeAllNodes()")
        return

    def replace(self, line, old, new):
        """ Replaces text on a specified line and updates the IDE """
        try:

            # Store cursor
            origin = self.text.index(INSERT)
            # Get contents of the line
            a = index(line, 0)
            b = index(line, END)
            contents = self.text.get(a, b)
            # Find the part to replace

            i = contents.index(old)
            j = i + len(old)
            a = index(line, i)
            b = index(line, j)
            
            self.text.delete(a, b)
            self.text.insert(a, new)

            self.update(insert=a)

            self.text.mark_set(INSERT, origin)

        except:

            return

    def replace_re(self, line, new=""):
        """ Replaces text on a specified line and updates the IDE """
        try:

            # Store cursor
            origin = self.text.index(INSERT)
            # Get contents of the line
            a = index(line, 0)
            b = index(line, END)
            contents = self.text.get(a, b)

            # Search using RegEx
            match = re_pat(contents)

            if match:

                # Find the part to replace
                i = match.start()
                j = match.end()
                a = index(line, i)
                b = index(line, j)
                
                self.text.delete(a, b)
                self.text.insert(a, new)

                self.update(insert=a)

                self.text.mark_set(INSERT, origin)

        except Exception as e:

            print(e)

            return

    def set_all(self, text):
        self.text.delete("1.0", END)
        self.text.insert("1.0", text.strip())
        self.update_all()
        return

    def get_all(self):
        return self.text.get("1.0", END)

    def openhomepage(self):
        webbrowser.open("www.foxdot.org")
        return

    def opendocumentation(self):
        webbrowser.open("https://github.com/Qirky/FoxDot/tree/master/docs/FoxDot/lib")
        return
    
