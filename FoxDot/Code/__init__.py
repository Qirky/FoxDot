from __future__ import division

import sys
from types import CodeType, FunctionType, TypeType
from traceback import format_exc as error_stack
from when_statements import when
from ..Patterns.Operations import modi


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
    def __call__(self, code, verbose=True):
        """ Takes a string of FoxDot code and executes as Python """

        if not code: return

        try:

            if type(code) != CodeType:

                if verbose is True:

                    print stdout(code)

                    try:

                        sys.displayhook(eval(code, self.namespace))

                    except:

                        pass

                code = compile(code, "FoxDot", "exec")

            exec code in self.namespace

        except:

            print error_stack()

            raise

        return

execute = FoxDotCode()

def stdout(code):
    """ Shell-based output """
    console_text = code.strip().split("\n")
    return ">>> {}".format("\n... ".join(console_text))

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
