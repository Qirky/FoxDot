# -*- coding: cp1252 -*-
"""
    This module deals with the user interface and connecting the code written here
    in foxdot to the python code to supercollider. All live coding stuff should be
    in "env"

"""

from Tkinter import *
from threading import Thread
from time import sleep as wait
from env import foxdot
from design import *

# Function for getting index in an easier way

def index(index1, index2=None):
    if type(index1) == str and index2 == None:
        return [int(n) for n in index1.split('.')]
    
    return str(index1) + '.' + str(index2)

def empty(string):
    return len(string.replace(' ','')) == 0

# What

def load(fn=None):
    string = ""
    if fn:
        string += ""
    else:
        string += "from env import *"
    return string


# DEFINE KEY VARIABLES

# Keywords

keywords = ['def','while','for','class']

whitespace = " \t\n\r\f\v"

SC_Location = "C:\Program Files (x86)\SuperCollider-3.6.6"

f = open('startup.scd')
SynthDefs = f.read()
f.close()

# DEFINE 

# Root Widget

root = Tk()
root.title("FoxDot - Live Coding with Python and SuperCollider")

# App object

class App:

    def __init__(self, master):

        # Create Y scrollbar

        self.Yscroll = Scrollbar(master)
        self.Yscroll.pack(side=RIGHT, fill=Y)

        # Create text box

        self.text = Text(master, padx=5, pady=5, height=40, width=120, yscrollcommand=self.Yscroll.set)
        self.text.focus_set()

        # Key bindings
        self.text.bind("<Control-Return>", self.get_code)
        self.text.bind("<Control-a>", self.selectall)
        self.text.bind("<Control-.>", self.killall)
        self.text.bind("<Return>", self.newline)
        self.text.bind("<BackSpace>", self.delete)
        self.text.bind("<Tab>", self.tab)

        #self.text.bind("<Key>", self.update)

        # Automatic brackets

        self.left_brackets  = ["(","[","{","'",'"']
        self.right_brackets = [")","]","}","'",'"']

        self.all_brackets = dict([(self.left_brackets[i], char) for i, char in enumerate(self.right_brackets)])
        self.bracket_q = []
        
        for char in self.left_brackets + self.right_brackets:
            self.text.bind(char, self.brackets)

        # Set tag names and config for specific colours

        self.text.tag_config("functions", background="White", foreground="#FF9900")
        self.text.tag_config("key_types", background="White", foreground="#9900FF")
        self.text.tag_config("user_defn", background="White", foreground="#0000FF")
        self.text.tag_config("comments" , background="White", foreground="#FF3300")
        self.text.tag_config("text" ,     background="White", foreground="#000000")

        self.text.pack(fill=BOTH, expand = 1)

        # Default values

        self.tabsize = 4

        # Import libs

        self.send_to_env( load() )

    def update(self, event=None):
        """ Update the IDE on a keypress """

        if event.char not in python_kw_chars + ['(']: return

        # Get index and walk backwards until we ge a whitespace or column = 0

        end = self.text.index(INSERT)

        self.text.insert(end, event.char)        

        line, column = index(end)

        while column > 0:

            column -= 1

            if self.text.get(index(line, column)) in whitespace + '(':

                break


        # Now we have our for word start

        start = index(line, column)

        # Get colour marker and set colour

        word = self.text.get(start, end)

        is_text = True

        for kw_type, word_set in python_kw.items():

            for word in word_set:

                line, column = index(end)

                #print word, self.text.get(start, index(line, column + 1))

                if self.text.get(start, index(line, column + 1)) == word:

                    self.text.tag_add(kw_type, start, end)

                    is_text = False

                    break

        if is_text:

            # Remove tags

            for tag in python_kw:

                self.text.tag_remove(tag, start, end)

            self.text.tag_add('text', start, end)

        return "break"
                    

    def brackets(self, event):

        # If a right bracket is typed and was auto added, delete it

        if self.bracket_q and event.char == self.bracket_q[-1]:

            line, column = index(self.text.index(INSERT))

            if self.text.get(index(line, column)) == self.bracket_q[-1]:
    
                self.text.delete(index(line, column))

            self.bracket_q.pop(0)

        # If a left bracket, automatically add the right

        if event.char in self.left_brackets and self.text.get(self.text.index(INSERT)) in list(whitespace) + self.left_brackets + self.right_brackets:
            
            # Insert closed brackets

            self.text.insert(self.text.index(INSERT), self.all_brackets[event.char])

            # Move cursor back one place

            line, column = index(self.text.index(INSERT))

            self.text.mark_set("insert", "%d.%d" % (line, column - 1))

            # Add to the stack of "open brackets"

            self.bracket_q.append(self.all_brackets[event.char])

        # Add originally typed bracket

        self.text.insert(self.text.index(INSERT), event.char)

        return "break"

    def send_to_env(self, code_str):

        """ Handles code execution and name space management """

        foxdot.execute( code_str )        
            
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

        Thread(target=self.highlight, args=(a,b)).start()

        # Execute the python code
        
        self.send_to_env( self.text.get( a , b ) )

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

        # Hold highlight
        
        wait(0.2)

        # Unhighlight
        
        self.text.tag_config("code", background="White", foreground="Black")

        # Remove labels

        self.text.tag_delete("code")

        return
                
    def newline(self, event):
        """ Elegantly goes to the next line """
        left  = list("({[")
        right = list(")}]") 
        
        # Look for last open bracket character
        i, j = index(self.text.index(INSERT))
        line = self.text.get("%d.0" % i, "%d.end" % i)

        n = 0
        enclosed = 0

        for n in range(len(line)-1,-1,-1):
            char = line[n]
            if char in right:
                enclosed += 1
            if char in left and enclosed:
                enclosed -= 1
            elif char in left and not enclosed: # look for spaces
                n+=1
                try:
                    while line[n] == " ":
                        n+=1
                except:
                    pass
                break

        # If n = 0, check for leading whitespace to keep in line
        
        if n == 0 and not enclosed and not empty(line):
            while line[n:].startswith(' '):
                n+=1

        # Keywords to tab with

        try:

            if line.split()[0] in keywords and j == len(line):
                n += self.tabsize

        except:

            pass
            
        
        # Add the amount of whitespace

        whitespace = n

        # Add new line
        self.text.insert(self.text.index(INSERT), "\n")

        # Add whitespace
        self.text.insert(self.text.index(INSERT), " " * whitespace)
        
        return "break"

    def tab(self, event):
        # TODO tab forward a whole selection
        self.text.insert(self.text.index(INSERT), self.tabspace())
        return "break"
    
    def tabspace(self):
        return " " * self.tabsize

    def delete(self, event):
        # If there is a selected area, delete that
        try:
            self.text.delete(SEL_FIRST, SEL_LAST)
            return "break"
        except:
            pass

        # Else, work out if there is a tab to delete
        
        i, j = index(self.text.index(INSERT))

        tab = index(i,j-self.tabsize)
        cur = index(i,j)
        char_l = self.text.get(index(i,j-1))
        char_r = self.text.get(index(i,j+1))  
        
        # Check if there's a tab
        if self.text.get(tab,cur) == self.tabspace():
            self.text.delete(tab, cur)
            return "break"

        # Check if in a set of empty brackets and delete both
        elif char_l in self.left_brackets:
            for b in self.left_brackets:
                if b == self.text.get(index(i,j-1)) and self.all_brackets[b] == self.text.get(cur):
                    self.text.delete(index(i, j-1), index(i,j+1))
                    return "break"
                
                
        # Delete 1 char
        elif j > 0:
            self.text.delete(index(i, j-1))
            self.update(event)            
            return "break"

    def selectall(self, event):
        self.text.tag_add(SEL, "1.0", END)
        self.text.mark_set(INSERT, "1.0")
        self.text.see(INSERT)
        return 'break'

    def killall(self, event):

        self.send_to_env("clock_.clear()")
        
        return "break"
  

if __name__ == "__main__":

    # Instantiate App

    app = App(root)

    # Run

    root.mainloop()
