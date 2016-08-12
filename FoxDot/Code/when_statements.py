from func_cmp import func_cmp

class _whenStatement:

    def __init__(self, func):
        self.expr = func

        self.action = lambda: None
        self.notaction = lambda: None
        
        self.do_switch = False
        self.elsedo_switch = False

    def evaluate(self):
        # Call and execute
        if self.expr():
            if not self.do_switch:
                self.action()
                self.do_switch = True
                self.elsedo_switch = False
        else:
            if not self.elsedo_switch:
                self.notaction()
                self.do_switch = False
                self.elsedo_switch = True
                
    def do(self, func):
        if callable(func):
            self.action = func
        return self
    
    def elsedo(self, func):
        if callable(func):
            self.notaction = func
        return self
    
    def stop(self):
        pass

class _whenLibrary:
    """
        Example:
        
        when(lambda: x==10).do(lambda: p.shuffle()).elsedo(lambda: p. reverse())
                
        
    """
    metro = None
    dur   = 0.125
    def __init__(self):
        self.library = []
        self.scheduled = False
        
    def __call__(self, func=None, **kwargs):
        """ Calling when() with no arguments will evaluate all expressions
            stored in self.library. Calling with func as a valid function
            will see if the function is in self.library and add it if not,
            or update the 

        """
        # Calling with no argument executes the statements
        
        if func is None and self.scheduled:
            
            for expression in self.library:

                expression.evaluate()

            self.metro.schedule(self, self.metro.now() + self.dur)

        # Giving it a function will return the corresponding when statement
        # or create a new one if it doesn't exist
        
        elif callable(func):
            
            for stmt in self.library:

                if func_cmp(func, stmt.expr):

                    return stmt
            else:

                # Make a new statement

                self.library.append(_whenStatement(func))

                # Schedule in the clock
        
                if not self.scheduled:

                    self.metro.schedule(self, self.metro.now() + self.dur)
                    self.scheduled = True

                # Return the last added expression

                return self.library[-1]

        return self

    def reset(self):
        """ Clears the library and stop scheduling """
        self.library = []
        self.scheduled = False
        return self

when = _whenLibrary()
