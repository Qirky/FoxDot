""" Repeat.py """

from Code import WarningMsg
from Patterns import asStream, modi

        

class Repeatable:
    def __init__(self):
        self.repeat_events = {}        

    def after(self, n, cmd, *args, **kwargs):
        """ Schedule self.cmd(args, kwargs) in n beats """
        return self
        
    def every(self, n, cmd, *args, **kwargs):
        """ Every n beats, do self.cmd(args) """

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

        # If the method call already exists, just update it

        if cmd in self.repeat_events:

            self.repeat_events[cmd].update(n, args, kwargs)

            if not self.repeat_events[cmd].isScheduled():

                self.repeat_events[cmd].schedule()

        else:

            call = MethodCall(self, method, n, args, kwargs)

            self.repeat_events[cmd] = call

            call.schedule()

        return self


class MethodCall:
    """ Class to represent an object's method call that,
        when called, schedules itself in the future """
    def __init__(self, parent, method, n, args=(), kwargs={}):
        self.parent = parent      
        # self.name = method
        self.method = method
        self.when = asStream(n)
        self.i    = 0
        self.next = self.when[self.i] + self.parent.metro.next_bar()
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        """ Proxy for parent object __call__ """

        self.i += 1
        self.next += modi(self.when, self.i)

##        # Get arguments for this call
##        if type(self.args) is tuple:
##            args = [modi(arg, self.i) for arg in self.args]
##        else:
##            args = [modi(self.args, self.i)]

        # Call the parent's method
        # getattr(self.parent, self.name).__call__(*args)
        self.method.__call__(*self.args, **self.kwargs)

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

    def update(self, n, args=(), kwargs={}):
        self.when = asStream(n)
        self.args = args
        self.kwargs = kwargs
        return self
