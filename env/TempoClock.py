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

        self.queue = [[] for n in range( len(self) ) ]

        self.beat = 0

        self.playing = []

        self.ticking = False
        
        threading.Thread(target=self.start).start()

    def __str__(self):

        return "clock"

    def __iter__(self):

        for x in self.queue:

            yield x

    def __len__(self):

        return int( self.steps * self.beats() )

    def beats(self):

        return int(self.timeSig[0] * self.bars)

    def real_beat(self):

        return self.beat / self.steps

    def bar_length(self):

        return int(self.timeSig[0] * self.steps)

    def beat_dur(self):

        return float( 60.0 / self.bpm )

    def step_dur(self):

        return float( self.beat_dur() / self.steps )

    def beatsPerBar(self):

        return self.timeSig[0]

    def now(self):

        return self.beat % len(self.queue)

    def start(self):

        self.ticking = True

        # Increases the timer by 8th beats
        
        while self.ticking:

            # Iterate through any players in the queues current set

            if self.beat % self.bar_length() == 0 :

                # Start any quantised players at new bar

                for player in self.playing:

                    if not player.isplaying:

                        player.event_n = 0

                        player.play()

            # Update and play players

            for player in self.queue[self.now()]:

                player.update()

                if player.isplaying:

                    player.send()

                # print self.beat % self.bar_length(),  player.now("degree"), player.event_n

            sleep( self.step_dur() )

            self.beat += 1

        return self

    def add2q(self, player, beat = 0):

        # Adds a player to the queue (default beat is 0)

        index = beat % len(self)

        if player not in self.queue[index]:

            self.queue[index].append(player)

        return

    def stop(self):

        self.ticking = False

        self.beat = 0

        return

    def clear(self):
        """ Remove players from clock """
        
        while len(self.playing) != 0:
            
            p = self.playing[0]
            p.stop()

        self.queue = [[] for n in range( len(self) ) ]

        self.beat = 0

        return
