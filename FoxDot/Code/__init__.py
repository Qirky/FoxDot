from __future__ import division
from types import CodeType, FunctionType
from traceback import format_exc as error_stack
import when_statements, player_objects, sample_players
import assignments

class LiveObject:
    foxdot_object = True
    isAlive = True
    def kill(self):
        self.isAlive = False
        return self

FoxDotSyntax = [ when_statements,
                 player_objects,
                 sample_players ]

def process(text, ns={}):
    """ Iterates over the modules that replace FoxDot syntax with Python """
    
    for syntax in FoxDotSyntax:

        text = syntax.find(text)

    text = assignments.check(text, ns)

    return text

def execute(code, verbose=True):
    """ Takes a string of FoxDot code and executes as Python """

    namespace = globals()

    try:

        if type(code) != CodeType:

            code = process(code, namespace)

            if verbose: print stdout(code)

            if not code:

                return

            else:

                code = compile(code, "FoxDot", "exec")

        exec code in namespace

    except:

        print error_stack()

        raise # raise the error to any foxdot code that executes foxdot code

    return


def stdout(code):
    """ Imitates the Python IDE output style """
    
    console_text = code.strip().split("\n")

    return ">>> %s" % "\n>>> ".join(console_text)
