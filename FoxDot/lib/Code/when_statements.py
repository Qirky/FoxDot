from func_cmp import *
from threading import Thread

class _whenStatement:

    def __init__(self, func):
        self.expr = func
        self.reset()
        self.remove_me = False

    def __repr__(self):
        return func_str(self.expr)

    def reset(self):
        self.action = lambda: None
        self.notaction = lambda: None
        self.do_switch = False
        self.elsedo_switch = False

    def evaluate(self):
        # Call and execute
        if self.expr():
            if not self.do_switch:
                self.action()
                self.toggle_live_functions(True)
                self.do_switch = True
                self.elsedo_switch = False
        else:
            if not self.elsedo_switch:
                self.notaction()
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
                
    def do(self, func):
        if callable(func):
            self.action = func
        return self
    
    def elsedo(self, func):
        if callable(func):
            self.notaction = func
        return self
    
    def stop(self):
        self.reset()
        return self

    def remove(self):
        self.reset()
        self.remove_me = True
        return self

class _whenLibrary:
    """
        Example:
        
        A. when(lambda: x==10).do(lambda: p.shuffle()).elsedo(lambda: p. reverse())               
        
    """
    def __init__(self):
        self.library = []
        
    def start_thread(self):
        self.thread = Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def __len__(self):
        return len(self.library)

    def __repr__(self):
        return repr(self.library)

    def run(self):
        """ Continual loop evaluating when_statements
        """
        while True:
            
            for expression in self.library:

                if expression.remove_me == True:

                    self.library.remove(expression)

                    if len(self.library) == 0:

                        break

                else:

                    expression.evaluate()

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

            if len(self.library) == 0:

                self.start_thread()                
            
            for stmt in self.library:

                if func_cmp(func, stmt.expr):

                    return stmt

            else:

                # Make a new statement

                self.library.append(_whenStatement(func))

                # Return the last added expression

                return self.library[-1]

        else:

            print("{} is not callable".format(func))

        return self

    def reset(self):
        """ Clears the library and stop scheduling """
        self.library = []
        return self

when = _whenLibrary()
