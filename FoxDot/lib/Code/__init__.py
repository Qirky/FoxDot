from __future__ import division

import sys
from types import CodeType, FunctionType, TypeType
from traceback import format_exc as error_stack
from when_statements import when
from live_functions import livefunction
from ..Patterns.Operations import modi

# Player RegEx
import re
re_player = re.compile(r"(\s*?)(\w+)\s*?>>\s*?\w+")

"""
    Live Object
    ===========

    Base for any self-scheduling objects

"""

class LiveObject(object):

    foxdot_object = True
    isAlive = True
    
    metro = None
    step  = None
    n     = 0
    
    def kill(self):
        self.isAlive = False
        return self

    def __call__(self):
        self.metro.schedule(self, self.metro.now() + float(modi(self.step, self.n)))
        self.n += 1
        return self

"""
    FoxCode
    =======
    Handles the execution of FoxDot code
    
"""

class FoxDotCode:
    namespace={}
    player_line_numbers={}
    def __call__(self, code, verbose=True):
        """ Takes a string of FoxDot code and executes as Python """

        if not code: return

        try:

            if type(code) != CodeType:

                response = stdout(code)

                if verbose is True:

                    print(response)
                    
                code = compile(code, "FoxDot", "exec")

            exec code in self.namespace

        except:

            response = error_stack()

            print(response)

        #TODO - Add sys.displayhook?

        return response

    def update_line_numbers(self, text_widget, start="1.0", end="end", remove=0):

        lines = text_widget.get(start, end).split("\n")[remove:]
        update = []
        offset = int(start.split(".")[0])

        for i, line in enumerate(lines):

            # Check line for a player and assign it a line number
            match = re_player.match(line)
            line_changed = False

            if match is not None:                

                whitespace = len(match.group(1))
                player     = match.group(2)
                line       = i + offset

                if player in self.player_line_numbers:

                    if (line, whitespace) != self.player_line_numbers[player]:

                        line_changed = True

                if line_changed or player not in self.player_line_numbers:

                    self.player_line_numbers[player] = (line, whitespace)
                    update.append("{}.id = '{}'".format(player, player))
                    update.append("{}.line_number = {}".format(player, line))
                    update.append("{}.whitespace  = {}".format(player, whitespace))

        # Execute updates if necessary
    
        if len(update) > 0:

            self.__call__("\n".join(update), verbose = False)
                
        return

execute = FoxDotCode()

""" Returns the value of objects if they are time-varying """
def get_now(obj):
    return getattr(obj, 'now', lambda: obj).__call__()

""" Printing / Formatting functions """

def stdout(code):
    """ Shell-based output """
    console_text = code.strip().split("\n")
    return ">>> {}".format("\n... ".join(console_text))

def WarningMsg(text):
    print("Warning: {}".format( text ))

""" These functions return information about an imported module """

def classes(module):
    """ Returns a list of class names defined in module """
    return [name for name, data in vars(module).items() if type(data) == TypeType]

def instances(module, cls):
    """ Returns a list of instances of cls from module """
    return [name for name, data in vars(module).items() if isinstance(data, cls)]

def functions(module):
    """ Returns a list of function names defined in module """
    return [name for name, data in vars(module).items() if type(data) == FunctionType]
