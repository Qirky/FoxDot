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

    def new_queue(self):

        try:

            return [n for n in self.queue][:len(self)] + [[] for n in range(abs(len(self)-len(self.queue))) ]

        except:

            return [[] for n in range( len(self) ) ]

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

            # Iterate through any players in the queues current set

            if self.beat % self.bar_length() == 0 :

                # Start any quantised players at new bar

                for player in self.playing:

                    if not player.isplaying:

                        player.event_n = 0

                        player.play()

            # Update and play players

            for player in self.queue[self.now()]:

                if player.isplaying:

                    player.update()

                    player.send()

                # print self.beat % self.bar_length(),  player.now("degree"), player.event_n

            sleep( self.step_dur() )

            self.beat += 1

            # Check if the time signature, steps, or bars values have been changed

            if old_steps != self.steps or old_timeSig != self.timeSig or old_bars != self.bars:

                # Change the queue size

                self.queue = self.new_queue()

                # Update our "old" values

                old_steps   = self.steps
                old_timeSig = self.timeSig
                old_bars    = self.bars

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
            p.kill()

        self.queue = [[] for n in range( len(self) ) ]

        self.beat = 0

        return
