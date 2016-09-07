"""

    TempoClock.py
    =============
    
    Clock management

"""

from Players import PlayerObject
from Patterns import asStream
from TimeVar import var
from Patterns.Operations import modi
from time import sleep, time
from sys import maxint as MAXINT
import threading
import Code
line = "\n"

class TempoClock:

    def __init__(self, bpm=120.0, meter=(4,4)):

        self.bpm = bpm

        self.time = 0
        self.mark = time()

        self.ts = meter
        
        self.queue = []
        self.nextEvent = None

        self.ticking = False        

        # Keeps track of the when statements and players

        self.when_statements = {}
        self.playing = []

        # If one object is going to played

        self.solo = SoloPlayer()

    def __str__(self):

        return str(self.queue)

    def __iter__(self):

        for x in self.queue:

            yield x

    def __len__(self):

        return len(self.queue)

    def Bar(self):
        """ Returns the length of a bar in terms of beats """
        return (float(self.ts[0]) / self.ts[1]) * 4

    def BeatDuration(self):
        """ Returns the length in seconds of one beat """
        return 60.0 / float(self.bpm)

    def beat(self, n):
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


    def run(self):

        self.ticking = True

        # Sleep until next event

        while self.ticking:

            if self.now() >= self.nextEvent:

                try:

                    event = self.queue.pop()

                    for n in range(len(event[0])-1, -1, -1):

                        item = event[0][n]

                        if callable(item):
                            
                            item()

                except IndexError:

                    pass

            if len(self.queue) == 0:

                self.nextEvent = MAXINT

            rest = max((self.nextEvent - self.now()) * 0.25, 0)
            sleep(min(self.beat(1), rest))

        return

    def sleep(self):
        
        return None

    def schedule(self, obj, beat=None):
        """ Add a player / event to the queue """

        if self.ticking == False:

            self.start()

        # Default is next bar

        if beat is None:

            beat = self.NextBar()

        # Keep track of objects in the Clock

        if obj not in self.playing and isinstance(obj, PlayerObject):

            self.playing.append(obj)

        # Go through queue and add in order

        for i in range(len(self.queue)):

            # If another event is happening at the same time, schedule together

            if beat == self.queue[i][1]:

                if isinstance(obj, PlayerObject):

                    self.queue[i][0].append(obj)

                else:

                    self.queue[i][0].insert(0, obj)

                break

            if beat > self.queue[i][1]:

                self.queue.insert(i, ([obj], beat))

                break
            
        else:
            
            self.queue.append(([obj], beat))

        # Set next event time

        self.nextEvent = self.queue[-1][1]
            
        return

    def NextBar(self):
        """ Returns the beat value for the start of the next bar """
        beat = self.now()
        return beat + (self.ts[0] - (beat % self.ts[0]))

    def get_bpm(self):
        try:
            bpm = float(self.bpm.now(self.time))
        except:
            bpm = float(self.bpm)
        return bpm

    def NextEvent(self):
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

##    def when(self, a, b, step=0.125, nextBar=False):
##        """
##
##            When Statements
##            ===============
##
##            Clock.When(a, b[,step])
##
##            When 'a' is true, do 'b'. Check this every step.
##
##        """
##
##        if nextBar:
##
##            start = self.NextBar()
##
##        else:
##
##            start = self.now() + step
##
##        w = When(a, b, step, self)
##        
##        self.schedule(w, start)
##
##        self.when_statements[a] = w
##
##        return

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

                try:

                    player.kill()

                except:

                    pass

        for event in self.queue:

            for player in event[0]:

                try:

                    player.kill()

                except:

                    pass

        self.solo.reset()
        self.queue = []
        self.playing = []
        self.ticking = False
        self.reset()

        return

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
        


##class When(Code.LiveObject):
##    """
##
##        When Statements
##        ===============
##
##        TODO
##
##    """
##
##    def __init__(self, test, code, step, clock):
##
##        if type(code) in (list, tuple):
##            code = line.join(code)
##
##        self.metro = clock
##        self.test  = test
##        self.step  = step
##        self.code  = self.check(code)
##        self.n     = 0
##
##    @staticmethod
##    def check(code):
##        """ Test for syntax errors """
##        return compile(code, "FoxDot" , 'exec') if type(code) == str else code
##
##    def __call__(self, *args):
##        if type(self.code) == Code.FunctionType:
##            self.code()
##        else:
##            Code.execute(self.code, verbose=False)
##
##        Code.LiveObject.__call__(self)
##        
##        return
##
##    def __repr__(self):
##        return "< 'When %s'>" % str(self)
##
##    def __str__(self):
##        return self.test
##
##    def __eq__(self, other):
##        return str(self) == str(other)
##
##    def update(self, new, step=0.25):
##        if isinstance(new, When):
##            self.code = self.check(new.code)
##            self.step = new.step
##        else:
##            self.code = self.check(new)
##            self.step = step
##        return        
##
##    
