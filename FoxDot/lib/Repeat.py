""" Repeat.py """

from Code import WarningMsg
from Patterns import asStream, modi

        

class Repeatable(object):
    def __init__(self):
        self.repeat_events = {}        

    def after(self, n, cmd, *args, **kwargs):
        """ Schedule self.cmd(args, kwargs) in n beats """
        quantise = kwargs.get("quantise", True)

        try:

            event = lambda: getattr(self, cmd)(*args, **kwargs)

            if not quantise:

                time = self.metro.now() + n

            else:

                time = self.metro.next_bar() + n

            self.metro.schedule( event, time )

        except:

            pass
        
        return self
        
    def every(self, n, cmd, *args, **kwargs):
        """ Every n beats, call a method (defined as a string) on the
            object and use the args and kwargs. To call the method
            every n-th beat of a timeframe, use the `cycle` keyword argument
            to specify that timeframe.

            ```
            # Call the shuffle method every 4 beats

            p1.every(4, 'shuffle')

            # Call the stutter method on the 5th beat of every 8 beat cycle

            p1.every(5, 'stutter', 4, cycle=8)
            
            ```

        """

        try:

            # Make sure cmd is a method

            attr = cmd.split(".")

            if len(attr) == 1:
                method = getattr(self, attr[0])

            elif len(attr) == 2:

                #sub_method = getattr(self.attr[attr[0]], attr[1])

                sub_method = lambda *args, **kwargs: getattr(self.attr[attr[0]], attr[1]).__call__(*args, **kwargs)

                method = lambda *args, **kwargs: self.attr.update({attr[0]: sub_method(*args, **kwargs)})

            assert callable(method)

        except:

            WarningMsg("{} is not a valid method for type {}".format(cmd, self.__class__))

            return self

        # Collect the cycle length

        cycle = kwargs.get("cycle", None)

        kwargs = {key: value for key, value in kwargs.items() if key != "cycle"}

        # If the method call already exists, just update it

        key = ('every', cmd)

        if key in self.repeat_events:

            self.repeat_events[key].update(n, cycle, args, kwargs)

            if not self.repeat_events[key].isScheduled():

                self.repeat_events[key].schedule()

        else:

            call = MethodCall(self, method, n, cycle, args, kwargs)

            self.repeat_events[key] = call

            call.schedule()

        return self

class MethodCall:
    """ Class to represent an object's method call that,
        when called, schedules itself in the future """
    def __init__(self, parent, method, n, cycle=None, args=(), kwargs={}):
        
        self.parent = parent  
        self.method = method

        self.cycle = cycle
        self.when  = asStream(n)

        self.this_when = self.when[0]
        self.last_when = 0
        
        self.i    = 0
        
        self.next = self.parent.metro.next_bar() + self.this_when

        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        return "<Future {}() call of '{}' player>".format(self.method.__name__, self.parent.synthdef)

    def __call__(self, *args, **kwargs):
        """ Proxy for parent object __call__ """

        self.i += 1

        self.last_when, self.this_when = self.this_when, modi(self.when, self.i)

        if self.cycle:
            
            self.next += (modi(self.cycle, self.i) + (self.this_when - self.last_when))

        else:

            self.next += self.this_when

        try:

            self.method.__call__(*self.args, **self.kwargs)

        except Exception as e:

            print("{} in '{}': {}".format(e.__class__.__name__, self.method.__name__, e))

        # Re-schedule the method call
        self.schedule()

        return

    def schedule(self):
        self.parent.metro.schedule(self, self.next)

    def isScheduled(self):
        """ Returns True if this is in the Tempo Clock """
        return self in self.parent.metro

    def stop(self):
        del self.parent.repeat_events[self.name]

    def update(self, n, cycle, args=(), kwargs={}):
        """ Updates the values of the MethodCall. Re-adjusts
            the index if cycle has been changed """
        self.when = asStream(n)
        self.args = args
        self.kwargs = kwargs

        if cycle is not None and cycle != self.cycle:

            self.next = self.parent.metro.next_bar() + self.when[self.i]

        self.cycle = cycle
        
        return self

class WhenModMethodCall(MethodCall):
    def __init__(self, parent, method, mod, n, args=(), kwargs={}):
        MethodCall.__init__(self, parent, method, n, args, kwargs)
        self.mod    = mod

    def __call__(self):
        """ Proxy for parent object __call__ """

        self.i += 1
        self.next += (self.mod + (self.when[self.i] - self.when[self.i-1]))

        self.method.__call__(*self.args, **self.kwargs)

        # Re-schedule the method call
        self.schedule()

        return
