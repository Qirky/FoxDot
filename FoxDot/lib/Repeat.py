from __future__ import absolute_import, division, print_function

from .Code import WarningMsg
from .Patterns import Pattern, Cycle, asStream
from .Utils import modi
from .TimeVar import var, Pvar

import inspect

class MethodList:
    """ Class for holding information about the order of which methods have been
        called on Player attributes. `root` is the original Pattern.
     """
    def __init__(self, root):
        self.root=root
        self.list_of_methods = []

    def get_root_pattern(self):
        return self.root

    def set_root_pattern(self, new):
        self.root = new

    def add_method(self, method_name, args, kwargs):
        self.list_of_methods.append((method_name, args, kwargs))

    def update(self, method, args, kwargs):
        """ Updates the args and kwargs for a repeated method """
        for i, info in enumerate(self.list_of_methods):
            name, _, _  = info
            if name == method:
                self.list_of_methods[i] = (method, args, kwargs)
                return
        raise ValueError

    def remove(self, method):
        """ Removes a method (should be a string) from the list of methods """
        for i, info in enumerate(self.list_of_methods):
            name, args, kwargs = info
            if name == method:
                self.list_of_methods.pop(i)
                return
        raise ValueError

    def __repr__(self):
        return repr(self.list_of_methods)

    def __contains__(self, method):
        """ Returns true if the method is in the list of methods """
        for name, args, kwargs in self.list_of_methods:
            if name == method:
                return True
        return False

    def __iter__(self):
        for value in self.list_of_methods:
            yield value

class Repeatable(object):
    after_update_methods = []
    method_synonyms      = {}
    def __init__(self):
        self.repeat_events        = {}
        self.previous_patterns    = {} # not a good name - TODO change

    def update_pattern_root(self, attr):
        """ Update the base attribute pattern that methods are applied to """

        if attr not in self.previous_patterns:

            self.previous_patterns[attr] = MethodList(self.attr[attr])

        else:

            self.previous_patterns[attr].set_root_pattern( self.attr[attr] )

        self.update_pattern_methods(attr)     

        return

    def update_pattern_methods(self, attr):
        """ Update the 'current' version of a pattern based on its root and methods stored """

        if attr not in self.previous_patterns:

            self.previous_patterns[attr] = MethodList(self.attr[attr])

        result = self.previous_patterns[attr].get_root_pattern()

        # For each method in the list, call on the pattern

        for method, args, kwargs in self.previous_patterns[attr]:

            call_pattern_method = getattr(Pattern, method)

            result = call_pattern_method(result, *args, **kwargs)

        self.attr[attr] = result

        return

    def get_attr_and_method_name(self, cmd):
        """ Returns the attribute and method name from a string in the form
            `"attr.method"` would return `"attr"` and `"method"`. If attr is not
            present, it returns `"degree"` in place. 
        """

        if cmd in self.method_synonyms:

            attr = [ self.method_synonyms[cmd] ]

        else:

            attr = cmd.split(".")

        # We can also schedule attribute methods

        if len(attr) == 1:

            attr_name   = "degree"
            method_name = attr[0]

        elif len(attr) == 2:

            attr_name = attr[0]
            method_name = attr[1]

        return attr_name, method_name

    def is_pattern_method(self, method_name, attr="degree"):
        """ Returns True if the method is a valid method of `Pattern` """

        if attr == "degree" and hasattr(self, method_name):

            return False

        elif hasattr(Pattern, method_name):

            return True

        else:

            return False

    def is_player_method(self, method_name, attr="degree"):
        """ Returns True if the method is a valid method  of `Player` """ 
        return hasattr(self, method_name) and attr == "degree"

    def get_method_by_name(self, cmd):
        """ Returns the attribute name and method based on `cmd` which is a string.
            Should be in form `"attr.method"`.
        """

        attr_name, method_name = self.get_attr_and_method_name(cmd)

        # Just get the player method if a valid player method

        if self.is_player_method(method_name, attr_name):

            method = getattr(self, method_name)

        # If its a Pattern method, create a "new" function  that acts as a method

        elif self.is_pattern_method(method_name, attr_name):

            def method(*args, **kwargs):

                # If there are no "old" patterns held in memory, use the pattern method and store

                if attr_name not in self.previous_patterns:

                    self.previous_patterns[attr_name] = MethodList(self.attr[attr_name]) # store the root

                # If this has already been called, "undo it"

                if method_name in self.previous_patterns[attr_name]:

                    self.previous_patterns[attr_name].remove(method_name)

                # If not, add it to the list

                else:

                    self.previous_patterns[attr_name].add_method(method_name, args, kwargs)

                # Update the attribute

                self.update_pattern_methods(attr_name)

                return

            method.__name__ = cmd # for debugging purposes

        else:

            # Raise TypeError if not a method

            err = "{} is not a valid method for type {}".format(cmd, self.__class__)
            
            raise(TypeError(err))

        assert callable(method)
        
        return attr_name, method

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
        
    def every(self, occurence, cmd, *args, **kwargs):
        """ Every n beats, call a method (defined as a string) on the
            object and use the args and kwargs. To call the method
            every n-th beat of a timeframe, use the `cycle` keyword argument
            to specify that timeframe.

            ::
                # Call the shuffle method every 4 beats

                p1.every(4, 'shuffle')

                # Call the stutter method on the 5th beat of every 8 beat cycle

                p1.every(5, 'stutter', 4, cycle=8)

                # If the method is not valid but *is* a valid Pattern method, that is called and reverted

                p1.every(4, 'palindrome')
        """

        try:

            attr, method = self.get_method_by_name(cmd)

        except AttributeError:

            WarningMsg("{} is not a valid method for type {}".format(cmd, self.__class__))

            return self

        # Collect the cycle length

        cycle = None
        ident = None

        if "cycle" in kwargs:

            cycle = kwargs["cycle"]
            del kwargs["cycle"]

        if "ident" in kwargs:

            ident = kwargs["ident"]
            del kwargs["ident"]

        # Convert `Cycles` to `var`-- should they be Pvar?

        attr_name, method_name = self.get_attr_and_method_name(cmd)

        # Just get the player method if a valid player method

        if self.is_player_method(method_name, attr_name):

            cycle_dur = occurence

        else:

            cycle_dur = occurence * 2

        args, kwargs = self.convert_cycles(args, kwargs, cycle_dur)

        # If the method call already exists, just update it (should be in a function)

        if ident is not None:

            cmd = "{}-{}".format(cmd, ident)

        if cmd in self.repeat_events:

            # Work out whether the method needs calling or not

            call = self.repeat_events[cmd]

            # Update the time details

            call.update(occurence, cycle, args, kwargs)

            attr, method_name = self.get_attr_and_method_name(cmd)

            if self.is_pattern_method(method_name, attr):

                # if n is even, it means the method is active # TODO -- put this in a class mate

                n, acc = call.count()

                if n % 2 == 1:

                    if method_name in self.previous_patterns[attr]:

                        self.previous_patterns[attr].remove(method_name)

                else:

                    if method_name in self.previous_patterns[attr]:

                        self.previous_patterns[attr].update(method_name, args, kwargs)

                # Update the attribute

                self.update_pattern_methods(attr)

            if not call.isScheduled():

                call.schedule()

        else:

            self.repeat_events[cmd] = MethodCall(self, method, occurence, cycle, args, kwargs)

            self.repeat_events[cmd].schedule()

        return self

    def stop_calling_all(self):
        """ Stops all repeated methods. """
        for method in list(self.repeat_events.keys()):

            self.never(method)

        return self            

    def never(self, cmd, ident=None):
        """ Stops calling cmd on repeat """

        attr, method = self.get_attr_and_method_name(cmd)

        if ident is not None:
        
            cmd = "{}-{}".format(cmd, ident)

        try:
            # If it a pattern method, undo it
            
            if method in self.previous_patterns[attr]:
            
                self.previous_patterns[attr].remove(method)
            
                self.update_pattern_methods(attr)
            
            self.repeat_events[cmd].stop()
            
            del self.repeat_events[cmd]
        
        except KeyError:
        
            err = "Player method '{}' not active".format(cmd)
        
            raise KeyError(err)
        
        return self

    @staticmethod
    def convert_cycles(args, kwargs, occurence):
        """ Converts any values that are instances of `Cycle` to a `var` with the 
            same duration as the frequency of the every call (occurrence) """

        args = [(var(value, occurence) if isinstance(value, Cycle) else value) for value in args]
        kwargs = {key: (var(value, occurence) if isinstance(value, Cycle) else value) for key, value in kwargs.items()}

        return args, kwargs

class MethodCall:
    """ Class to represent an object's method call that,
        when called, schedules itself in the future """
    def __init__(self, parent, method, n, cycle=None, args=(), kwargs={}):
        
        self.parent = parent  
        self.method = method

        self.update(n, cycle, args, kwargs)

        self.after_update = False
        self.stopping = False

    def update(self, n, cycle=None, args=(), kwargs={}):
        """ Updates the values of the MethodCall. Re-adjusts the index if cycle has been changed """

        if cycle is not None:

            self.when   = asStream(cycle)
            self.cycle  = asStream(n)

        else:

            self.when   = asStream(n)
            self.cycle  = None

        self.args = args
        self.kwargs = kwargs

        # Check if a method has the _beat_ keyword argument

        if "_beat_" in inspect.getfullargspec(self.method).args:

            self.kwargs["_beat_"] = None

        self.i, self.next = self.count()

        self.offset = float(modi(self.cycle, self.i)) if self.cycle is not None else 0
        
        return self

    def count(self):
        """ Counts the number of times this method would have been called between clock start and now """

        n = 0; acc = 0; dur = 0
        now = float(self.parent.metro.now())

        # Get durations

        durations = self.when # if self.cycle is None else asStream(self.cycle)
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

                acc += dur
                n   += 1

                if acc >= now:

                    break

        return n, acc

    def __repr__(self):
        return "<Future {}() call of '{}'>".format(self.method.__name__, self.parent)

    def __call__(self, *args, **kwargs):
        """ Proxy for parent object __call__, calls the enclosed method and schedules it in the future. """

        assert self.method is not None

        # Return without scheduling if stopping
        
        if self.stopping:

            return

        # Give the method a reference to when OSC messages should send

        self.assign_beat()

        # Call the method

        self.call_method()

         # Update the next time to schedule

        self.next += float(self.when[self.i])

        if self.cycle is not None:
            
            self.offset = float(modi(self.cycle, self.i))

        # Re-schedule the method call

        self.schedule()

        # Increase the index to get the next duration
        
        self.i += 1

        return

    def assign_beat(self):
        if "_beat_" in self.kwargs:
            self.kwargs["_beat_"] = self.get_next()
        return

    def call_method(self):
        """ Calls the method. Prints to the console with error info. """
        try:

            self.method.__call__(*self.args, **self.kwargs)

        except Exception as e:

            print("{} in '{}': {}".format(e.__class__.__name__, self.method.__name__, e))

        return

    def get_next(self):
        """ Returns the beat that the next occurrence of this method call is due """
        return self.next + self.offset

    def schedule(self):
        """ Schedules the method to be called in the clock """
        self.parent.metro.schedule(self, self.get_next())

    def isScheduled(self):
        """ Returns True if this is in the Tempo Clock """
        return self in self.parent.metro

    def stop(self):
        self.stopping = True
