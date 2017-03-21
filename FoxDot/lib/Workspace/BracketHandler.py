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

        self.style = bracket_formatting

        self.left_brackets = dict(zip(left_b, right_b))
        self.right_brackets = dict(zip(right_b, left_b))

        self.queue = []

        for char in self.left_brackets.keys() + self.right_brackets.keys():

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

                self.text.insert(b, self.left_brackets[event.char])
                self.text.insert(a, event.char)

                # unselect

                self.text.tag_remove(SEL, "1.0", END)

                ret = "break"
                
            except:
                
                pass

            # B. Needs a closing bracket

            if next_char in whitespace + self.right_brackets.keys() and next_char not in ("'", '"'):

                self.text.insert(self.text.index(insert), event.char + self.left_brackets[event.char])

                self.text.mark_set(insert, index(line, column + 1))

                ret = "break"

            # Update line colours
        
            self.root.colour_line(line)

        # 2. Type right bracket
        elif event.char in self.right_brackets:

            # Go back and find an open bracket -> assume the first open bracket is related to *this* one

            self.text.insert("{}.{}".format(line,column), event.char) # Add bracket

            coords = self.find_starting_bracket(line, column, event.char)

            new_line, new_col = line, column + 1

            # Assume we are adding a new bracket

            adding_bracket = True

            # Get index of the end of the buffer

            end_line, end_col = index(self.text.index(END))

            while (new_line, new_col) != (end_line, end_col):

                # If we find a closing bracket,  find it's pair

                next_char = self.text.get(index(new_line, new_col))

                if next_char == event.char:

                    coords_ = self.find_starting_bracket(new_line, new_col, event.char, offset=0)

                    # If there is a closing brackets

                    if coords_ is None:

                        adding_bracket = False

                        break

                    else:

                        adding_bracket = True

                if index(new_line, new_col) == self.text.index(index(new_line, "end")):
                    
                    new_line += 1
                    new_col   = 0

                else:

                    new_col += 1
                
            if not adding_bracket:

                self.text.delete(index(line, column+1))

            ret = "break"

            # Update line colours
            
            self.root.colour_line(line)

            # Highlight brackets

            if coords is not None:

                row, col = coords

                self.text.tag_config("tag_open_brackets", **self.style)
                self.text.tag_add("tag_open_brackets", "{}.{}".format(row,col), "{}.{}".format(row,col+1))
                self.text.tag_add("tag_open_brackets", "{}.{}".format(line,column), "{}.{}".format(line,column+1))

                # Remove bracket highlight after 0.2 sec?

                # self.text.after(200, lambda: self.text.tag_delete("tag_open_brackets"))

        return ret

    def delete(self, insert=INSERT):
        line, column = index(self.text.index(insert))
        next_char    = self.text.get(index(line, column))
        prev_char    = self.text.get(index(line, column-1))

        if prev_char in self.left_brackets:
            if next_char == self.left_brackets[prev_char] and column > 0:
                self.text.delete(index(line, column-1), index(line, column+1))
                return True
        return False

    def find_starting_bracket(self, line, column, bracket_style, offset = 0):
        """ Finds the opening bracket to the closing bracket at line, column co-ords.
            Returns None if not found. """
        
        line_length = column - 1
        used_br = offset

        for row in range(line, 0, -1):

            for col in range(line_length, -1, -1):

                # If the char is a left bracket and not used, break

                if self.text.get("{}.{}".format(row, col)) == self.right_brackets[bracket_style]:

                    # open_br += 1
                    if used_br == 0:

                        return row, col

                    else:

                        used_br -= 1

                elif self.text.get("{}.{}".format(row, col)) == bracket_style:

                    used_br += 1

            line_length = int(self.text.index("{}.end".format(row-1)).split(".")[1])

        else:

            return None
