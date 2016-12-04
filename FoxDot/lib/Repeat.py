""" Repeat.py """

from Code import WarningMsg
from Patterns import asStream, modi

class Repeatable:
    def __init__(self):
        self.repeat_events = {}
        
    def every(self, n, cmd, args=()):
        """ Every n beats, do self.cmd(args) """

        try:

            # Make sure cmd is a method

            method = getattr(self, cmd)

            assert callable(method)

        except:

            WarningMsg("{} is not a valid method for type {}".format(cmd, self.__class__))

            return self

        # Make sure args is a tuple

        try:

            args = tuple(args)

        except:

            args = (args,)

        # If the method call already exists, just update it

        if cmd in self.repeat_events:

            self.repeat_events[cmd].update(n, args)

            if not self.repeat_events[cmd].isScheduled():

                self.repeat_events[cmd].schedule()

        else:

            call = MethodCall(self, cmd, n, args)

            self.repeat_events[cmd] = call

            call.schedule()

        return self


class MethodCall:
    """ Class to represent an object's method call that,
        when called, schedules itself in the future """
    def __init__(self, parent, method, n, args=()):
        self.parent = parent      
        self.name = method
        self.when = asStream(n)
        self.i    = 0
        self.next = self.when[self.i] + self.parent.metro.next_bar()
        self.args = args

    def __call__(self):
        """ Proxy for parent object __call__ """

        self.i += 1
        self.next += modi(self.when, self.i)

        # Get arguments for this call
        if type(self.args) is tuple:
            args = [modi(arg, self.i) for arg in self.args]
        else:
            args = [modi(self.args, self.i)]

        # Call the parent's method
        getattr(self.parent, self.name).__call__(*args)

        # Re-schedule the method call
        self.schedule()

        return

    def schedule(self):
        self.parent.metro.schedule(self, self.next - 0.1)

    def isScheduled(self):
        """ Returns True if this is in the Tempo Clock """
        return self in self.parent.metro

    def stop(self):
        del self.parent.repeat_events[self.name]

    def update(self, n, args=()):
        self.when = asStream(n)
        self.args = args
        return self
