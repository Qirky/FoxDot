from Tkinter import *
from threading import Thread
from time import sleep as wait
from formatting import *

import sys

# Function for getting index in an easier way

def index(index1, index2=None):
    if type(index1) == str and index2 == None:
        return [int(n) for n in index1.split('.')]
    
    return str(index1) + '.' + str(index2)

def empty(string):
    return len(string.replace(' ','')) == 0

def isDelete(char):
    return char == "\x08"

def isReturn(char):
    return char == "\r"

def isHex(char):
    return len(repr(char)) > 3

def indented(s):
    for i, char in enumerate(s):
        if char != " ":
            break
    return i

def open_bracket(text):

    count = dict([(l,0) for l in left_b])

    for i, char in enumerate(text):

        if   char in left_b:

            count[char] += 1

        elif char in right_b:

            count[brackets[char]] -= 1

    open_br = [b for b in count.keys() if (count[b] >= max(count.values()) > 0) and (count[b] % 2 == 1) ]

    pos = [text.rfind( b ) for b in open_br]

    if pos:

        return max(pos) + 1

def function(text):

    tokens = text.strip()

    if tokens[-1] != ":":

        return

    tokens = tokens[:-1]
    
    for b in left_b + right_b:
        
        tokens = tokens.replace(b," ")

    tokens = tokens.split()

    for kw in py_indent_kw:

        if kw in tokens:

            return indented(text) + tabsize
 

class console:
    """ Console widget that displays the true Python input """

    def __init__(self, master):

        self.Yscroll = Scrollbar(master)
        self.Yscroll.pack(side=RIGHT, fill=Y)        
        
        self.text = Text( master, padx=5, pady=5,
                            height=10, width=120,
                            bg="Black", fg="White",
                            font=("Ubuntu Mono", 12),
                            yscrollcommand=self.Yscroll.set)

        self.Yscroll.config(command=self.text.yview)

        self.text.bind("<Key>", lambda e: "break")

        self.text.pack(fill=BOTH, expand=1)

    def __str__(self):

        return self.text.get()        

    def write(self, string):

        # Add text
        self.text.insert( END, string )

        # Scroll down
        self.text.see(END)

        return

    def read(self):

        return str(self)
        

# App object

class App:

    def __init__(self):

        # Set up master widget  

        self.root = Tk()
        self.root.title("FoxDot - Live Coding with Python and SuperCollider")
        self.root.protocol("WM_DELETE_WINDOW", self.kill )

        # Create Y scrollbar

        self.Yscroll = Scrollbar(self.root)
        self.Yscroll.pack(side=RIGHT, fill=Y)

        # Create text box for code

        self.text = Text(self.root,
                         padx=5, pady=5,
                         height=20, width=100,
                         bg = colour_map['background'],
                         fg=colour_map['plaintext'],
                         insertbackground="White",
                         font = ("Ubuntu Mono", 12),
                         yscrollcommand=self.Yscroll.set)

        self.Yscroll.config(command=self.text.yview)
        
        self.text.focus_set()

        # Key bindings
        self.text.bind("<Control-Return>", self.get_code)
        self.text.bind("<Control-a>", self.selectall)
        self.text.bind("<Control-.>", self.killall)
        self.text.bind("<Return>", self.newline)
        self.text.bind("<BackSpace>", self.delete)
        self.text.bind("<Delete>", self.delete2)
        self.text.bind("<Tab>", self.tab)
        self.text.bind("<Key>", self.keypress)

        # Automatic brackets

        self.separators = py_separators

        self.left_brackets  = ["(","[","{","'",'"']
        self.right_brackets = [")","]","}","'",'"']

        self.all_brackets = dict([(self.left_brackets[i], char) for i, char in enumerate(self.right_brackets)])
        self.bracket_q = []
        
        for char in self.left_brackets + self.right_brackets:
            self.text.bind(char, self.brackets)

        # Set tag names and config for specific colours

        for name, colour in colour_map.items():
            self.text.tag_config(name, foreground=colour)

        # Pack the text box

        self.text.pack(fill=BOTH, expand = 1)

        # Create lable for console

        self.console = console(self.root)

        sys.stdout = self.console

    def run(self):
        """ Starts the Tk mainloop for the master widget """

        print "Welcome to FoxDot!"

        self.root.mainloop()

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

    def update(self, event=None):

        # Move the window to view the current line

        self.text.see(INSERT)

        # 1. Get the contents of the current line

        cur = self.text.index(INSERT)

        line, column = index(cur)

        # -- check current and last line if return key

        lines = [line] + [line-1] * int(isReturn(event.char))

        for line in lines:

            start, end = index(line,0), index(line,"end")

            thisline = self.text.get(start, end)

            # 2. Remove tags at current point

            for tag_name in self.text.tag_names():

                self.text.tag_remove(tag_name, start, end)

            # 3. Update IDE

            for tag_name, start, end in findstyles(thisline):

                self.text.tag_add(tag_name, index(line, start), index(line, end))

        return "break"
                    

    def brackets(self, event):

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

    def submit(self, code_str):

        """ This method needs to be overwritten for sending code to your environment """
    
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
        """ Execute in a separate thread """

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

        # Hold highlight
        
        wait(0.2)

        # Remove labels

        self.text.tag_delete("code")

        return

    def newline(self, event):

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
        # TODO tab forward a whole selection
        self.text.insert(self.text.index(INSERT), self.tabspace())
        return "break"
    
    def tabspace(self):
        return " " * tabsize

    def delete_selection(self):
        """ If an area is selected, it is deleted and returns True """
        try:
            self.text.delete(SEL_FIRST, SEL_LAST)
            return True
        
        except:
            return False

    def delete2(self, event):
        self.update(event)
        return
    
    def delete(self, event):
        # If there is a selected area, delete that
        if self.delete_selection():
            return "break"
        

        # Else, work out if there is a tab to delete
        
        i, j = index(self.text.index(INSERT))

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

    def selectall(self, event):
        self.text.tag_add(SEL, "1.0", END)
        self.text.mark_set(INSERT, "1.0")
        self.text.see(INSERT)
        return 'break'

    def killall(self, event):
        """ Ctrl+. function to be defined by the user """
        
        return

    def terminate(self):
        """ To be overridden by user to be called on window close """

        return

    def kill(self):

        self.terminate()

        self.root.destroy()

        return
