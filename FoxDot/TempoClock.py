# Clock management

from Patterns import asStream
from Patterns.Operations import modi
import threading
from time import sleep, time
from sys import maxint as MAXINT

class TempoClock:

    def __init__(self, bpm=120.0, time_signature=(4,4)):

        self.bpm = bpm

        self.time = 0
        self.mark = time()

        self.time_signature = time_signature
        
        self.queue = []

        self.ticking = False        

        # Keeps track of the when statements and players

        self.when_statements = {}
        self.playing = []

    def __str__(self):

        return str(self.queue)

    def __iter__(self):

        for x in self.queue:

            yield x

    def __len__(self):

        return len(self.queue)

    def Bar(self):
        """ Returns the length of a bar in terms of beats """
        return (float(self.time_signature[0]) / self.time_signature[1]) * 4

    def BeatDuration(self):
        """ Returns the length in seconds of one beat """
        return 60.0 / self.bpm

    def now(self):
        """ Adds to the current counter and returns its value """
        now = time()
        self.time += (now - self.mark) * (self.bpm  / 60.0)
        self.mark = now
        return self.time
        
    def start(self):
        """ Starts the clock thread """
        threading.Thread(target=self.run).start()
        return

    def run(self):
        """ Main loop """        

        self.ticking = True
        self.beat = 0
 
        while self.ticking:
                        
            # Update and play players at next event

            now = self.now()

            if int(now) > self.beat:

                self.beat = int(now)

            if self.now() >= self.NextEvent():

                event = self.queue.pop()

                for player in event[0]:

                    player()

        return self

    def Schedule(self, player, beat):
        """ Add a player / event to the queue """

        # Go through queue and add in order

        for i in range(len(self.queue)):

            # If another event is happening at the same time, schedule together

            if beat == self.queue[i][1]:

                self.queue[i][0].append(player)

                break

            if beat > self.queue[i][1]:

                self.queue.insert(i, ([player], beat))

                break
            
        else:
            
            self.queue.append(([player], beat))
            
        return

    def NextBar(self):
        """ Returns the beat value for the start of the next bar """
        beat = self.now()
        return beat + (self.time_signature[0] - (beat % self.time_signature[0]))

    def NextEvent(self):
        """ Returns the beat index for the next event to be called """
        try:    return self.queue[-1][1]
        except: return MAXINT
        

    def When(self, a, b, step=0.125, nextBar=False):
        """

            When Statements
            ===============

            Clock.When(a, b[,step])

            When 'a' is true, do 'b'. Check this every step.

        """

        if nextBar:

            start = self.NextBar()

        else:

            start = self.now() + step

        w = When(a, b, step, self)
        
        self.Schedule(w, start)

        self.when_statements[a] = w

        return

    def stop(self):

        self.ticking = False

        self.beat = 0

        return

    def clear(self):
        """ Remove players from clock """

        for event in self.queue:

            for player in event[0]:

                player.kill()

        self.queue = []

        self.start_time = time()

        self.beat = 0

        return

class Infinity(int):
    """
        Infinity Object
        ===============

        Is the length of time of one clock cycle

    """

    def __new__(cls, metro):

        return int.__new__(cls, len(metro))


import Code
line = "\n"

class When(Code.LiveObject):
    """

        When Statements
        ===============

        TODO

    """

    def __init__(self, test, code, step, clock):

        if type(code) in (list, tuple):
            code = line.join(code)

        self.metro = clock
        self.test  = test
        self.step  = step
        self.code  = self.check(code)
        self.n     = 0

    @staticmethod
    def check(code):
        """ Test for syntax errors """
        return compile(code, "FoxDot" , 'exec') if type(code) == str else code

    def __call__(self, *args):
        if type(self.code) == Code.FunctionType:
            self.code()
        else:
            Code.execute(self.code, verbose=False)

        self.metro.Schedule(self, self.metro.now() + modi(self.step, self.n))
        self.n += 1
        
        return

    def __repr__(self):
        return "< 'When %s'>" % str(self)

    def __str__(self):
        return self.test

    def __eq__(self, other):
        return str(self) == str(other)

    def update(self, new, step=0.25):
        if isinstance(new, When):
            self.code = self.check(new.code)
            self.step = new.step
        else:
            self.code = self.check(new)
            self.step = step
        return        

    
