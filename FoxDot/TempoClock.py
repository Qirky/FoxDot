"""

    TempoClock.py
    =============
    
    Clock management

"""

from Players import Player, PlayerKey
from Patterns import asStream
from TimeVar import var
from Patterns.Operations import modi
from time import sleep, time
from sys import maxint as MAXINT
import threading
import Code
line = "\n"

class TempoClock:

    when_statements = lambda: None

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
    

##    def BeatDuration(self):
##        """ Returns the length in seconds of one beat """
##        return 60.0 / float(self.bpm)

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
        threading.Thread(target=self.run).start()
        return

    def when_eval(self):
        """ Evaluates any 'when' statements """
        if len(self.when_statements) > 0:
            self.when_statements.__call__()
        return

    def run(self):

        self.ticking = True

        while self.ticking:

            # Evaluate when_statements at EVERY possible opportunity

            self.when_eval()            

            if self.now() >= self.queue.next():

                # Call any item in the popped event

                for item in self.queue.pop():    

                    item.__call__()

                    # Test if any changes caused by item.__call__() affect when statements

                    self.when_eval()

            # Make sure rest is positive so any events that SHOULD
            # have been played are played straight away
            rest = max((self.queue.next() - self.now()) * 0.25, 0)

            # If there are no events for at least 1 beat, sleep for 1 beat
            # sleep(min(self.beat(1), rest))
            sleep(min(0.005, rest))

        return

    def schedule(self, obj, beat=None):
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

        if beat > self.now():

            self.queue.add(obj, beat)
        
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
        except: return MAXINT

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

    def clear(self):
        """ Remove players from clock """

        for player in self.playing:

                player.reset()
                player.kill()

        self.items = []
        self.queue.clear()
        self.solo.reset()
        
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

    def add(self, item, beat):

        # If the new event is before the next scheduled event,
        # move it to the 'front' of the queue

        if beat < self.next():

            self.data.append(QueueItem(item, beat))

            return

        # If the event is after the next scheduled event, work
        # out its position in the queue

        for i in range(len(self.data)):

            # If another event is happening at the same time, schedule together

            if beat == self.data[i].beat:

                self.data[i].add(item)

                break

            # If the event is later than the next event, schedule it here

            if beat > self.data[i].beat:

                self.data.insert(i, QueueItem(item, beat))

                break            

        return

    def clear(self):
        while len(self.data):
            del self.data[-1]
        return

    def pop(self):
        return self.data.pop() if len(self.data) > 0 else []

    def next(self):
        return self.data[-1].beat if len(self.data) > 0 else MAXINT
            

class QueueItem:
    def __init__(self, obj, t):

        # Priority
        self.players_high = []
        self.players_low  = []
        self.other        = []

        self.beat = t
        self.add(obj)
        
    def __repr__(self):
        return "{}: {}".format(self.beat, self.players_high + self.players_low + self.other)
    
    def add(self, obj):
        
        # High priority

        if isinstance(obj, Player):

            # High priority player objects *do not* contain PlayerKey attributes

            if any([isinstance(attr, PlayerKey) for attr in obj.attr.values()]):

                self.players_low.append(obj)

            else:

                self.players_high.append(obj)

        # None player objects have lowest priority

        else: self.other.append(obj)

        return
    
    def call(self):
        """ Calls all items in queue slot """
        for item in self:
            item.__call__()
        return
    
    def __iter__(self):
        
        for item in self.players_high + self.players_low + self.other:

            yield item

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
