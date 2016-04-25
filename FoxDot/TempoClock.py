# Clock management

import threading
from time import sleep

class TempoClock:

    def __init__(self, bpm=120.0, bars=16, steps=8, timeSig=(4,4)):

        self.bpm = bpm

        # How many steps per beat, default is 8

        self.bars    = bars

        self.timeSig = timeSig
        
        self.steps   = steps

        # Create queue based on loop and steps

        self.queue = self.new_queue()
        
        self.beat = 0

        self.playing = []

        self.ticking = False

        # List of "code" objects

        self.when_statements = []

    def __str__(self):

        return "TempoClock Object @ %.2f bpm, %d/%d" % (self.bpm, self.timeSig[0], self.timeSig[1])

    def __iter__(self):

        for x in self.queue:

            yield x

    def __len__(self):

        return int( self.steps * self.beats() )

    def change_steps(self, new=8):

        self.steps = new
        self.queue = self.new_queue()

    def polyrhythm(self, a, b):

        self.timeSig = (a,b)

        self.change_steps( a*b )

        return        

    def new_queue(self):

        return [[] for n in range( len(self) ) ]

    def reset(self):

        self.queue = self.new_queue()

        for p in self.playing:

            p.update_clock()

        return
        

    def beats(self):

        return int(self.timeSig[0] * self.bars)

    def real_beat(self):

        return self.beat / self.steps

    def bar_length(self):

        return int(self.timeSig[0] * self.steps)

    def beat_dur(self):

        return float( 60.0 / float(self.bpm) )

    def step_dur(self):

        return float( self.beat_dur() / self.steps )

    def til_next_bar(self):

        return (len(self)-self.now()) % self.bar_length()

    def beatsPerBar(self):

        return self.timeSig[0]

    def now(self):

        return self.beat % len(self.queue)

    def start(self):

        threading.Thread(target=self.run).start()

        return

    def run(self):

        self.ticking = True

        old_steps   = self.steps
        old_timeSig = self.timeSig
        old_bars    = self.bars

        # Increases the timer by 8th (default) beats
  
        while self.ticking:

            # Execute any When statements

            for code in self.when_statements:

                if self.beat % code(self.steps) == 0:

                    try:

                        code.run()

                    except:

                        self.when_statements.remove(code)

            # Iterate through any players in the queues current set

            if self.beat % self.bar_length() == 0 :

                # Start any quantised players at new bar

                for player in self.playing:

                    if not player.isplaying:

                        # Player is updated BEFORE first OSC msg, so event_n is set to -1 to compensate

                        player.event_n = -1

                        player.play()

            # Update and play players

            step = self.queue[self.now()]

            for player in step:

                if player.isplaying:

                    player.update_state()

                    player.send()

            # Rest
            
            sleep( self.step_dur() )

            self.beat += 1

            # Check if the time signature, steps, or bars values have been changed

            if old_steps != self.steps: # or old_timeSig != self.timeSig or old_bars != self.bars:

                # Change the queue size

                self.reset()

                # Update our "old" values

                old_steps   = self.steps
                #old_timeSig = self.timeSig
                #old_bars    = self.bars

        return self

    def add2q(self, player, beat = 0):

        # Adds a player to the queue (default beat is 0)

        index = beat % len(self)

        if player not in self.queue[index]:

            self.queue[index].append(player)

        return

    def when(self, a, b, step=None):

        print a, b

        if step is not None:

            when = When(a, b, step)

        else:

            when = When(a, b)

        print when in self.when_statements

        if when not in self.when_statements:

            self.when_statements.append( when )

        else:

            i = self.when_statements.index( when )

            self.when_statements[i].update( when.code )

        return

    def stop(self):

        self.ticking = False

        self.beat = 0

        return

    def clear(self):
        """ Remove players from clock """
        
        while len(self.playing) != 0:
            
            p = self.playing[0]
            p.kill()

        while len(self.when_statements) != 0:

            del self.when_statements[0]

        self.queue = [[] for n in range( len(self) ) ]

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

class When:
    """

        When Statements
        ===============

        TODO

    """

    def __init__(self, test, code, step=0.25):
        """ code is exectuted. test is evaluated every quarter beat by default """

        if type(code) in (list, tuple):
            code = line.join(code)

        self.test = test
        self.step = step
    
        # Test for syntax errors
        if type(code) == str:
            self.code = compile(code, "FoxDot" , 'exec')
        else:
            self.code = code
        
    def __mod__(self, n):
        """ Returns 1 if n % 1/step is 0 """
        return int( (n % (1.0 / self.step)) == 0 )

    def __call__(self, steps_per_beat):
        return int(self.step * steps_per_beat)

    def __repr__(self):
        return "< 'When %s'>" % str(self)

    def __str__(self):
        return self.test

    def __eq__(self, other):
        return str(self) == str(other)

    def update(self, new):
        self.code = new
        return

    def run(self):
        if type(self.code) == Code.FunctionType:
            self.code()
        else:
            Code.execute(self.code, verbose=False)
        return

    
