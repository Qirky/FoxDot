from __future__ import absolute_import, division, print_function

from .Code import WarningMsg
from .Patterns import asStream
from .Utils import modi

class Repeatable(object):
    after_update_methods = []
    method_synonyms      = {}
    def __init__(self):
        self.repeat_events        = {}

    def after(self, n, cmd, *args, **kwargs):
        """ Schedule self.cmd(args, kwargs) in 'n' beats time
            ```
            # Stop the player looping after 16 beats
            p1 >> pads().after(16, "stop")
            ```
        """
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

            if cmd in self.method_synonyms:

                attr = [ self.method_synonyms[cmd] ]

            else:

                attr = cmd.split(".")

            # We can also schedule attribute methods

            if len(attr) == 1:

                method_name = attr[0]

                method = getattr(self, method_name)

            elif len(attr) == 2:

                # TODO -- add this functionality to PlayerKey class

                sub_method = lambda *args, **kwargs: getattr(self.attr[attr[0]], attr[1]).__call__(*args, **kwargs)

                method = lambda *args, **kwargs: self.attr.update({attr[0]: sub_method(*args, **kwargs)})

            assert callable(method)

        except:

            WarningMsg("{} is not a valid method for type {}".format(cmd, self.__class__))

            return self

        # Collect the cycle length

        cycle = kwargs.get("cycle", None)
        ident = kwargs.get("ident", None)

        kwargs = {key: value for key, value in kwargs.items() if key not in ("cycle", "ident")}

        # If the method call already exists, just update it

        if ident is not None:

            cmd = "{}-{}".format(cmd, ident)

        if cmd in self.repeat_events:

            self.repeat_events[cmd].update(n, cycle, args, kwargs)

            if not self.repeat_events[cmd].isScheduled():

                self.repeat_events[cmd].schedule()

        else:

            call = MethodCall(self, method, n, cycle, args, kwargs)

            self.repeat_events[cmd] = call

            call.schedule()

        return self

    def stop_calling_all(self):
        for method in list(self.repeat_events.keys()):
            self.never(method)
        return self
            

    def never(self, method):
        try:
            self.repeat_events[method].stop()
            del self.repeat_events[method]
        except KeyError:
            err = "Player method '{}' not active".format(method)
            raise KeyError(err)
        return self

class MethodCall:
    """ Class to represent an object's method call that,
        when called, schedules itself in the future """
    def __init__(self, parent, method, n, cycle=None, args=(), kwargs={}):
        
        self.parent = parent  
        self.method = method

        self.cycle = cycle
        self.when  = asStream(n)

        self.this_when = float(self.when[0])
        self.last_when = 0
        
        self.i, self.next = self.count()

        self.args = args
        self.kwargs = kwargs

        self.after_update = False

        self.stopping = False

    def count(self):
        """ Counts the number of times this method would have been called between clock start and now """

        n = 0
        acc = 0
        dur = 0
        now = float(self.parent.metro.now())

        # Get durations

        durations = self.when if self.cycle is None else asStream(self.cycle)
        total_dur = float(sum(durations))

        # How much time left to fit remainder in

        try:
       
            acc = now - (now % total_dur)

        except ZeroDivisionError:

            acc = 0

        # n is the index to return for calculating self.when[n]
        # acc is when to start

        n = int(len(durations) * (acc / total_dur))

        if acc != now:

            while True:

                dur = float(durations[n])

                if acc + dur == now:

                    acc += dur

                    n += 1

                    break

                elif acc + dur > now:

                    acc += dur
                    n += 1

                    break

                else:
                    
                    acc += dur
                    n += 1

        return n, acc

    def __repr__(self):
        return "<Future {}() call of '{}' player>".format(self.method.__name__, self.parent.synthdef)

    def __call__(self, *args, **kwargs):
        """ Proxy for parent object __call__, calls the enclosed method
            and schedules it in the future. """

        self.i += 1

        self.last_when, self.this_when = self.this_when, float(self.when[self.i])

        if self.cycle:
            
            self.next += (float(modi(self.cycle, self.i)) + (self.this_when - self.last_when))

        else:

            self.next += self.this_when

        try:

            self.method.__call__(*self.args, **self.kwargs)

        except Exception as e:

            print("{} in '{}': {}".format(e.__class__.__name__, self.method.__name__, e))

        # Re-schedule the method call

        if not self.stopping:

            self.schedule()

        return

    def schedule(self):
        self.parent.metro.schedule(self, self.next)

    def isScheduled(self):
        """ Returns True if this is in the Tempo Clock """
        return self in self.parent.metro

    def stop(self):
        self.stopping = True

    def update(self, n, cycle, args=(), kwargs={}):
        """ Updates the values of the MethodCall. Re-adjusts
            the index if cycle has been changed """
        self.when = asStream(n)
        self.args = args
        self.kwargs = kwargs

        self.i, self.next = self.count()

##        if cycle is not None and cycle != self.cycle:
##
##            self.next = self.parent.metro.next_bar() + self.when[self.i]

        self.cycle = cycle
        
        return self
