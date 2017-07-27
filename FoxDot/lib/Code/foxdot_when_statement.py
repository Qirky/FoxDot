"""
    How to use `when` statements
    ----------------------------

    A `when` statement is similar to your traditional `if` statement but
    instead of evaluating the expression at the time the code is run, it
    is constantly testing it to see if it is true.

    ```
    Example 1
    ---------

    when 5 < 10:
        print True
    else:
        print False
    ```

    Currently there is no `elif` statement implemented yet and lines of code
    cannot be spread over multiple lines.

    To "stop" an individual `when` statement from monitoring its test. You
    need to call the `__when__` object with a `lambda` expression equalling
    that of the test and call the `remove` method.

    ```
    Example 2
    ---------

    a, b = 5, 10

    when a > b:
        print "a is bigger"
    else:
        print "b is bigger"

    # This is how to 'stop' the statement above

    __when__(lambda: a > b).remove()

    # This removes *all* currently running when statements

    __when__.reset()
    ```

"""

from __future__ import absolute_import, division, print_function

from .foxdot_func_cmp import *
from threading import Thread
from time import sleep

class _whenStatement:

    namespace = {}

    def __init__(self, func):
        self.expr = func
        self.reset()
        self.remove_me = False

    def __repr__(self):
        return func_str(self.expr)

    @classmethod
    def set_namespace(cls, ns):
        ''' Define the namespace to execute the actions. Should be a `dict` '''
        cls.namespace = ns

    def reset(self):
        ''' Sets the `when` and `else` actions to nothing '''
        self.action = ()
        self.notaction = ()
        self.do_switch = False
        self.elsedo_switch = False

    def evaluate(self):
        ''' Calls the test expression, and if it has changed then
            run the appropriate response code '''
        if self.expr():
            if not self.do_switch:
                
                # Execute the values
                for action in self.action:
                    exec(compile(action, "FoxDot", "exec"), self.namespace)
                    
                self.toggle_live_functions(True)
                self.do_switch = True
                self.elsedo_switch = False
        else:
            if not self.elsedo_switch:
                
                # Execute the values
                for action in self.notaction:
                    exec(compile(action, "FoxDot", "exec"), self.namespace)

                self.toggle_live_functions(False)
                self.do_switch = False
                self.elsedo_switch = True

    def toggle_live_functions(self, switch):
        """ If the action functions are @livefunctions, turn them on/off """    
        try:
            self.action.live = switch
        except:
            pass
        try:
            self.notaction.live = (not switch)
        except:
            pass
        return
                
    def do(self, *instructions):
        ''' Set the instructions for when the test expression is True. Should
            be a list of strings. '''
        self.action = instructions
        return self
    
    def elsedo(self, *instructions):
        ''' Set the instructions for when the test expression is False. Should
            be a list of strings. '''
        self.notaction = instructions
        return self
    
    def stop(self):
        self.reset()
        return self

    def remove(self):
        self.reset()
        self.remove_me = True
        return self

class _whenLibrary:
    """  Used to store 'when statements'. Is accessed through the `__when__` object.
    """
    def __init__(self):
        self.library = []
        
    def start_thread(self):
        self.thread = Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    @staticmethod
    def set_namespace(env):
        _whenStatement.set_namespace(env.namespace)

    def __len__(self):
        return len(self.library)

    def __repr__(self):
        return repr(self.library)

    def run(self):
        """ Continual loop evaluating when_statements
        """
        while len(self.library) > 0:
            
            for expression in self.library[:]:

                if expression.remove_me == True:

                    self.library.remove(expression)

                else:

                    expression.evaluate()

            sleep(0.01)

        return
        
    def __call__(self, func=None, **kwargs):
        """ Calling when() with no arguments will evaluate all expressions
            stored in self.library. Calling with func as a valid function
            will see if the function is in self.library and add it if not,
            or update the 

        """

        # Giving it a function will return the corresponding when statement
        # or create a new one if it doesn't exist
        
        if callable(func):                
            
            for stmt in self.library:

                if func_cmp(func, stmt.expr):

                    return stmt

            else:

                # Make a new statement

                self.library.append(_whenStatement(func))

                # If that is the first statement, start the thread

                if len(self.library) == 1:

                    self.start_thread()

                # Return the last added expression

                return self.library[-1]

        else:

            print("{} is not callable".format(func))

        return self

    def reset(self):
        """ Clears the library and stop scheduling """
        self.library = []
        return self

__when__ = _whenLibrary()
