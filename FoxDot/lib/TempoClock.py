"""

    TempoClock.py
    =============
    
    Clock management

"""

from Players import Player, PlayerKey
from Repeat import MethodCall
from Patterns import asStream
from TimeVar import var
from Patterns.Operations import modi
from time import sleep, time
from traceback import format_exc as error_stack
import sys
import threading
import Code
line = "\n"

class TempoClock:

    # when_statements = lambda: None

    def __init__(self, bpm=120.0, meter=(4,4)):

        self.bpm = bpm
        self.time = 0
        self.mark = time()
        self.meter = meter
        self.queue = Queue()
        self.ticking = False        

        # Player Objects stored here
        self.playing = []

        # All other scheduled items go here
        self.items = []

        # If one object is going to played
        self.solo = SoloPlayer()

    def __str__(self):

        return str(self.queue)

    def __iter__(self):

        for x in self.queue:

            yield x

    def __len__(self):

        return len(self.queue)

    def __contains__(self, item):
        return item in self.items

    def bar_length(self):
        """ Returns the length of a bar in terms of beats """
        return (float(self.meter[0]) / self.meter[1]) * 4

    def beat(self, n=1):
        """ Returns the length of n beats in seconds """
        return (60.0 / float(self.bpm)) * n

    def now(self):
        """ Adds to the current counter and returns its value """
        now = time()
        if isinstance(self.bpm, var):
            bpm_val = self.bpm.now(self.time)
        else:
            bpm_val = self.bpm
        self.time += (now - self.mark) * (bpm_val  / 60.0)
        self.mark = now
        return self.time
        
    def start(self):
        """ Starts the clock thread """
        main = threading.Thread(target=self.run)
        main.daemon = True
        main.start()
        return

    def run(self):

        self.ticking = True

        while self.ticking:          

            if self.now() >= self.queue.next():

                # Call any item in the popped event

                block = self.queue.pop()

                for item in block:

                    if not block.called(item):
                        
                        try:

                            block.call(item)

                        except SystemExit:

                            sys.exit()

                        except:

                            print(error_stack())

            # Make sure rest is positive so any events that SHOULD
            # have been played are played straight away
            rest = max((self.queue.next() - self.now()) * 0.25, 0)

            # If there are no events for at least 1 beat, sleep for 1 beat
            # sleep(min(self.beat(1), rest))
            sleep(min(0.005, rest))

        return

    def schedule(self, obj, beat=None, args=(), kwargs={}):
        """ TempoClock.schedule(callable, beat=None)
            Add a player / event to the queue """

        if self.ticking == False:

            self.start()

        # Default is next bar

        if beat is None:

            beat = self.next_bar()

        # Keep track of objects in the Clock

        if obj not in self.playing and isinstance(obj, Player):

            self.playing.append(obj)

        if obj not in self.items:

            self.items.append(obj)

        # Add to the queue

##        try:

        if beat > self.now():

            self.queue.add(obj, beat, args, kwargs)

##        except Exception as e:
##
##            print e,  beat, self.now()

        # Add any events that should have happend, but silence Players
        
        else:

            if isinstance(obj, Player):

                kwargs['verbose'] = False
                
            self.queue.add(obj, self.now() + 0.1, args, kwargs)
        
        return

    def next_bar(self):
        """ Returns the beat value for the start of the next bar """
        beat = self.now()
        return beat + (self.meter[0] - (beat % self.meter[0]))

    def get_bpm(self):
        try:
            bpm = float(self.bpm.now(self.time))
        except:
            bpm = float(self.bpm)
        return bpm

    def next_event(self):
        """ Returns the beat index for the next event to be called """
        try:    return self.queue[-1][1]
        except: return sys.maxint

    def call(self, obj, dur, args=()):
        """ Returns a 'schedulable' wrapper for any callable object """
        return Wrapper(self, obj, dur, args)

    # Every n beats, do...

    def every(self, n, cmd, args=()):
        self.schedule(self.call(cmd, n, args))
        return

    def stop(self):
        self.ticking = False
        self.reset()
        return

    def reset(self):
        self.time = 0
        self.mark = time()
        return

    def shift(self, n):
        """ Offset the clock time """
        self.time += n
        return

    def clear(self):
        """ Remove players from clock """

        self.items = []
        self.queue.clear()
        self.solo.reset()

        for player in self.playing:

            player.reset()
            player.kill()

        for item in self.items:
            
            try: item.stop()
            except: pass                
        
        self.playing = []
        self.ticking = False
        self.reset()

        return

#####

class Queue:
    def __init__(self):
        self.data = []

    def __repr__(self):
        return "\n".join([str(item) for item in self.data]) if len(self.data) > 0 else "[]"

    def add(self, item, beat, args=(), kwargs={}):

        # If the new event is before the next scheduled event,
        # move it to the 'front' of the queue

        if beat < self.next():

            self.data.append(QueueItem(item, beat, args, kwargs))

            i = 0

        else:

            # If the event is after the next scheduled event, work
            # out its position in the queue

            for i in range(len(self.data)):

                # If another event is happening at the same time, schedule together

                if beat == self.data[i].beat:

                    self.data[i].add(item, args, kwargs)

                    break

                # If the event is later than the next event, schedule it here

                if beat > self.data[i].beat:

                    self.data.insert(i, QueueItem(item, beat, args, kwargs))

                    break

        # Tell any players about what queue item they are in

        if isinstance(item, Player):

            item.queue_block = self.data[i]

        return

    def clear(self):
        while len(self.data):
            del self.data[-1]
        return

    def pop(self):
        return self.data.pop() if len(self.data) > 0 else list()

    def next(self):
        return self.data[-1].beat if len(self.data) > 0 else sys.maxint
            
from types import FunctionType
class QueueItem:
    priority_levels = [
                        lambda x: type(x) == FunctionType,   # Any functions are called first
                        lambda x: isinstance(x, MethodCall), # Then scheduled player methods
                        lambda x: isinstance(x, Player),     # Then players themselves
                        lambda x: True                       # And anything else
                      ]
                       
    def __init__(self, obj, t, args=(), kwargs={}):

        self.events        = [ [] for lvl in self.priority_levels ]
        self.called_events = []
        self.called_objects = []

        self.beat = t
        self.add(obj, args, kwargs)
        
    def __repr__(self):
        return "{}: {}".format(self.beat, list(self))
    
    def add(self, obj, args=(), kwargs={}):

        q_obj = QueueObj(obj, args, kwargs)

        for i, level in enumerate(self.priority_levels):

            if level(obj):

                self.events[i].append(q_obj)

                break
        return

    def called(self, item):
        return item in self.called_events

    def call(self, item, caller = None):
        """ Calls all items in queue slot """
        # TODO -> Make more efficient
        
        if caller is not None:

            correct = (caller in self.objects())

            for event in self:

                if item == event.obj:

                    item = event

                    break

        else:

            correct = True

        # item is a QueueObj OR the object itself

        if correct and (item in self) and (item not in self.called_events):
            
            self[item].__call__()
            self.called_events.append(item)

        return

    def __getitem__(self, key):
        for event in self:
            # Possible need to be key.obj?
            if event == key:
                return event

    def __iter__(self):
        return (item for level in self.events for item in level)

    def objects(self):
        return [item.obj for level in self.events for item in level]
        

class QueueObj:
    def __init__(self, obj, args=(), kwargs={}):
        self.obj = obj
        self.args = args
        self.kwargs = kwargs
    def __eq__(self, other):
        return other == self.obj
    def __ne__(self, other):
        return other != self.obj
    def __repr__(self):
        return repr(self.obj)
    def __call__(self):
        self.obj.__call__(*self.args, **self.kwargs)

###############################################################
""" 
        TempoClock.Wrapper Class
        ========================

        Wraps any callable object as a self-scheduling object
        like a When() or Player() object.
        
"""

class Wrapper(Code.LiveObject):
    
    def __init__(self, metro, obj, dur, args=()):
        self.args  = asStream(args)
        self.obj   = obj
        self.step  = dur
        self.metro = metro
        self.n     = 0
        self.s     = self.obj.__class__.__name__

    def __str__(self):
        return "<Scheduled Call '%s'>" % self.s

    def __repr__(self):
        return  str(self)

    def __call__(self):
        """ Call the wrapped object and re-schedule """
        args = modi(self.args, self.n)
        try:
            self.obj.__call__(*args)
        except:
            self.obj.__call__(args)
        Code.LiveObject.__call__(self)

class SoloPlayer:
    """ SoloPlayer objects """
    def __init__(self):
        self.data = []

    def __repr__(self):
        if len(self.data) == 0:
            return "None"
        if len(self.data) == 1:
            return repr(self.data[0])
        else:
            return repr(self.data)
        
    def add(self, player):
        if player not in self.data:
            self.data.append(player)
    def set(self, player):
        self.data = [player]
    def reset(self):
        self.data = []
    def active(self):
        """ Returns true if self.data is not empty """
        return len(self.data) > 0
    def __eq__(self, other):
        """ Returns true if other is in self.data or if self.data is empty """
        return (other in self.data) if self.data else True
    def __ne__(self, other):
        return (other not in self.data) if self.data else True
