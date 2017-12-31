from __future__ import absolute_import, division, print_function

from .Code import WarningMsg
from .Patterns import Pattern, asStream
from .Utils import modi

class MethodList:
    def __init__(self, root):
        self.root=root
        self.list_of_methods = []
    def __repr__(self):
        return repr(self.list_of_methods)

    def remove(self, method):
        for i, info in enumerate(self.list_of_methods):
            name, args, kwargs = info
            if name == method:
                self.list_of_methods.pop(i)
                return
        raise ValueError

    def contains(self, method):
        for name, args, kwargs in self.list_of_methods:
            if name == method:
                return True
        return False

class Repeatable(object):
    after_update_methods = []
    method_synonyms      = {}
    def __init__(self):
        self.repeat_events        = {}
        self.previous_patterns    = {}

    def update_pattern_root(self, attr):

        if attr not in self.previous_patterns:

            self.previous_patterns[attr] = MethodList(self.attr[attr])

        else:

            self.previous_patterns[attr].root = self.attr[attr]

        self.update_pattern_methods(attr)     

        return

    def update_pattern_methods(self, attr):

        if attr not in self.previous_patterns:

            self.previous_patterns[attr] = MethodList(self.attr[attr])

        data = self.previous_patterns[attr].root

        for method, args, kwargs in self.previous_patterns[attr].list_of_methods:

            call_pattern_method = getattr(Pattern, method)

            data = call_pattern_method(data, *args, **kwargs)

        self.attr[attr] = data

        return

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

    def get_method_by_name(self, cmd):
         # Make sure cmd is a method

        if cmd in self.method_synonyms:

            attr = [ self.method_synonyms[cmd] ]

        else:

            attr = cmd.split(".")

        # We can also schedule attribute methods

        if len(attr) == 1:

            method_name = attr[0]

            if hasattr(self, method_name):

                method = getattr(self, method_name)

            elif hasattr(Pattern, method_name):

                # THIS ONLY CALLS ON DEGREE ATM                

                def method(*args, **kwargs):

                    # If there are no "old" patterns held in memory, use the pattern method and store

                    attr = "degree"

                    if attr not in self.previous_patterns:

                        self.previous_patterns[attr] = MethodList(self.attr[attr])

                    # If this has already been called, "undo it"

                    if self.previous_patterns[attr].contains(method_name):

                        self.previous_patterns[attr].remove(method_name)

                        # self.attr[attr] = call_pattern_method(self.attr[attr], *args, **kwargs)

                    # If not, add it to the list

                    else:

                        self.previous_patterns[attr].list_of_methods.append((method_name, args, kwargs))

                    # Update the attribute

                    self.update_pattern_methods(attr)

                    return

            else:

                WarningMsg("{} is not a valid method for type {}".format(cmd, self.__class__))

                return self

        elif len(attr) == 2:

            # TODO -- add this functionality to PlayerKey class?

            sub_method = lambda *args, **kwargs: getattr(self.attr[attr[0]], attr[1]).__call__(*args, **kwargs)

            method = lambda *args, **kwargs: self.attr.update({attr[0]: sub_method(*args, **kwargs)})

        assert callable(method)
        
        return method
        
    def every(self, occurence, cmd, *args, **kwargs):
        """ Every n beats, call a method (defined as a string) on the
            object and use the args and kwargs. To call the method
            every n-th beat of a timeframe, use the `cycle` keyword argument
            to specify that timeframe.

            ```
            # Call the shuffle method every 4 beats

            p1.every(4, 'shuffle')

            # Call the stutter method on the 5th beat of every 8 beat cycle

            p1.every(5, 'stutter', 4, cycle=8)

            # If the method is not valid but *is* a valid Pattern method, that is called and reverted

            p1.every(4, 'palindrome')
            
            ```

        """

        try:

            method = self.get_method_by_name(cmd)

        except AttributeError:

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

            self.repeat_events[cmd].update(occurence, cycle, args, kwargs)

            if not self.repeat_events[cmd].isScheduled():

                self.repeat_events[cmd].schedule()

        else:

            call = MethodCall(self, method, occurence, cycle, args, kwargs)

            self.repeat_events[cmd] = call

            call.schedule()

        return self

    def stop_calling_all(self):
        for method in list(self.repeat_events.keys()):
            self.never(method)
        return self
            

    def never(self, method):
        try:
            # If it a pattern method, undo it - so far this only applies to degree
            if self.previous_patterns["degree"].contains(method):
                self.previous_patterns["degree"].remove(method)
                self.update_pattern_methods("degree")
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

        # Return without scheduling if stopping
        
        if self.stopping:

            return

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

        if cycle is not None and cycle != self.cycle:

            self.next = self.parent.metro.next_bar() + self.when[self.i]

        self.cycle = cycle
        
        return self
