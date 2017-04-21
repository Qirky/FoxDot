"""

    TempoClock.py
    =============
    
    Clock management for scheduling notes and functions. Anything 'callable'
    can be scheduled and can also be 'wrapped' using `Clock.call`, which
    returns an object that schedules itself in the clock in the future once
    the wrapped object is called.

"""

from Players import Player, send_delay, func_delay
from Repeat import MethodCall
from Patterns import asStream
from TimeVar import var
from Midi import MidiIn, MIDIDeviceNotFound
from Patterns.Operations import modi
from time import sleep, time, clock
from fractions import Fraction
from traceback import format_exc as error_stack
import sys
import threading
import Code
line = "\n"

class TempoClock:

    def __init__(self, bpm=120.0, meter=(4,4)):

        # General set up
        self.bpm = bpm
        self.meter = meter

        # Start counting -- first call to clock() is 0
        self.time = 0 # time in secs
        self.beat = 0 # the number of beats
        self.start_time = time() # The time at start

        # Create the queue
        self.queue = Queue()
        self.current_block = None

        # Don't start yet...
        self.ticking = False
        
        # Midi Clock In
        self.midi_clock = None

        # Can be configured
        self.latency = 0.2
        self.sleep_time = 0.001

        # Debug
        self.debugging = False

        # Player Objects stored here
        self.playing = []

        # All other scheduled items go here
        self.items   = []

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

    def __setattr__(self, attr, value):
        if attr == "bpm":
            self.start_time = time()
            self.time       = 0.0
        self.__dict__[attr] = value

    def bar_length(self):
        """ Returns the length of a bar in terms of beats """
        return (float(self.meter[0]) / self.meter[1]) * 4

    def beat_dur(self, n=1):
        """ Returns the length of n beats in seconds """
        return (60.0 / float(self.bpm)) * n

    def get_latency(self):
        return self.latency

    def sync_to_midi(self, sync=True):
        """ If there is an available midi-in device sending MIDI Clock messages,
            this attempts to follow the tempo of the device. Requies rtmidi """
        try:
            if sync:
                self.midi_clock = MidiIn()
            elif self.midi_clock:
                self.midi_clock.close()
                self.midi_clock = None
        except MIDIDeviceNotFound as e:
            print("{}: No MIDI devices found".format(e))
        return

    def debug(self, on=True):
        self.debugging = bool(on)
        return

    def now(self):
        """ Returns the total elapsed time (in beats as opposed to seconds) """
        if isinstance(self.bpm, var):
            bpm_val = self.bpm.now(self.beat)
        elif self.midi_clock:
            bpm_val = self.midi_clock.bpm
        else:
            bpm_val = self.bpm

        # Update clock time
        
        now = time() - self.start_time

        self.beat += (now - self.time) * (bpm_val / 60.0)
            
        self.time = now

        return self.beat
        
    def start(self):
        """ Starts the clock thread """
        main = threading.Thread(target=self.run)
        main.daemon = True
        main.start()
        return

    def __run_block(self, block):
        """ Private method for calling all the items in the queue block.
            This means the clock can still 'tick' while a large number of
            events are activated  """

        # Call each item in turn (they can call each other if there are dependencies

        t1 = clock()
        
        for item in block:

            if not block.called(item):

                try:
                    block.call(item)

                except SystemExit:
                    sys.exit()

                except:
                    print(error_stack())

        t2 = clock()

        sleep_time = self.latency - (t2-t1)

        # If blocks are taking longer to iterate over than the latency, adjust accordingly

        if sleep_time < 0:

            self.latency -= sleep_time

            sleep_time = 0

        # Wait until the end of the latency period

        sleep(sleep_time)

        # Send all the message to supercollider together

        block.send_osc_messages()

        return

    def run(self):
        """ Main loop """
        
        self.ticking = True
        small_step = False

        while self.ticking:

            now        = self.now()
            next_event = self.queue.next()
            latency    = self.get_latency()

            delta = now - (next_event - latency)

            if delta >= 0:

                if self.debugging:

                    if delta > self.latency:

                        print("Late: {}".format(delta - self.latency))

                self.current_block = self.queue.pop()

                if len(self.current_block):

                    threading.Thread(target=self.__run_block, args=(self.current_block,)).start()

            if self.midi_clock is not None:

                self.midi_clock.update()

            sleep(self.sleep_time)

        return

    def set_time(self, beat):
        """ Set the clock time to 'beat' and update players in the clock """
        self.queue.clear()
        self.beat = beat
        self.time = time() - self.start_time
        for player in self.playing:
            player(count=True)
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

        if beat > self.now():

            self.queue.add(obj, beat, args, kwargs)

        # Add any events that should have happend, but silence Players
        
        else:

            if self.debugging:

                print "Object scheduled late:", obj, beat, self.now()

            if isinstance(obj, Player):

                kwargs['verbose'] = False

            self.queue.add(obj, self.now(), args, kwargs)
        
        return

    def next_bar(self):
        """ Returns the beat value for the start of the next bar """
        beat = self.now()
        return beat + (self.meter[0] - (beat % self.meter[0]))

    def get_bpm(self):
        if hasattr(self.bpm, 'now'):
            bpm = float(self.bpm.now(self.beat))
        else:
            bpm = float(self.bpm)
        return bpm

    def next_event(self):
        """ Returns the beat index for the next event to be called """
        return self.queue[-1][1]

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
        self.beat = 0
        self.time = time() - self.start_time
        return

    def shift(self, n):
        """ Offset the clock time """
        self.beat += n
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

            if hasattr(item, 'stop'):

                item.stop()             
        
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

            # i = 0

            block = self.data[-1]

        else:

            # If the event is after the next scheduled event, work
            # out its position in the queue

            # need to be careful in case self.data changes size

            # for i in range(len(self.data)):

            for block in self.data:

                # If another event is happening at the same time, schedule together

                #if beat == self.data[i].beat:
                if beat == block.beat:

                    #self.data[i].add(item, args, kwargs)
                    block.add(item, args, kwargs)                    

                    break

                # If the event is later than the next event, schedule it here

                #if beat > self.data[i].beat:
                if beat > block.beat:

                    i = self.data.index(block)

                    self.data.insert(i, QueueItem(item, beat, args, kwargs))

                    block = self.data[i]

                    break

        # Tell any players about what queue item they are in

        # if isinstance(item, Player):
        if hasattr(item, "queue_block"):

            # print item, block

            item.queue_block = block

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
                        lambda x: isinstance(x, func_delay), # Then scheduled functions
                        lambda x: isinstance(x, MethodCall), # Then scheduled player methods
                        lambda x: isinstance(x, send_delay), # Then delayed player messages
                        lambda x: isinstance(x, Player),     # Then players themselves
                        lambda x: True                       # And anything else
                      ]

    server = None
                       
    def __init__(self, obj, t, args=(), kwargs={}):

        self.events         = [ [] for lvl in self.priority_levels ]
        self.called_events  = []
        self.called_objects = []

        self.osc_messages   = []

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

    def send_osc_messages(self):
        for msg in self.osc_messages:
            self.server.client.send(msg)
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

    def __len__(self):
        return sum([len(level) for level in self.events])

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
        ### <> getting verbose error
        try:
            self.obj.__call__(*self.args, **self.kwargs)
        except TypeError as e:
            print self.obj, e
            print "QueuObj Call TypeError", self.kwargs

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
