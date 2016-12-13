from Tkinter import *
from Format import *
from AppFunctions import *

whitespace = [" ","\t","\n","\r","\f","\v"]

class BracketHandler:
    def __init__(self, master):

        self.root = master
        
        self.text = master.text

        self.inbrackets = False

        self.separators = py_separators

        self.left_brackets  = left_b

        self.right_brackets = right_b

        self.all_brackets = dict(zip(self.left_brackets, self.right_brackets))

        self.queue = []

        for char in self.left_brackets + self.right_brackets:

            self.text.bind(char, self.handle)

    def handle(self, event=None, insert=INSERT):

        ret = None

        line, column = index(self.text.index(insert))

        # 1. Type a left bracket

        next_char = self.text.get(index(line, column))

        if event.char in self.left_brackets:

            # A. Type a left bracket and an area is selected

            try:

                a = self.text.index(SEL_FIRST)
                b = self.text.index(SEL_LAST)

                self.text.insert(b, self.all_brackets[event.char])
                self.text.insert(a, event.char)

                # unselect

                self.text.tag_remove(SEL, "1.0", END)

                ret = "break"
                
            except:
                
                pass

            # B. Needs a closing bracket

            if next_char in whitespace + self.right_brackets:

                self.text.insert(self.text.index(insert), event.char + self.all_brackets[event.char])

                self.text.mark_set(insert, index(line, column + 1))

                ret = "break"

        # 2. Type right bracket
        elif event.char in self.right_brackets:

            # if there is *the same* right bracket in front of it, just move the cursor

            if next_char == event.char:

                self.text.mark_set(insert, index(line, column + 1))

                ret = "break"

            # TODO - highlight the enclosed area

        # Update line colours
        
        self.root.colour_line(line)

        return ret

    def delete(self, insert=INSERT):
        line, column = index(self.text.index(insert))
        next_char    = self.text.get(index(line, column))
        prev_char    = self.text.get(index(line, column-1))

        if prev_char in self.left_brackets:
            if next_char == self.all_brackets[prev_char] and column > 0:
                self.text.delete(index(line, column-1), index(line, column+1))
                return True
        return False
