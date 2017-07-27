"""

    TempoClock.py
    =============
    
    Clock management for scheduling notes and functions. Anything 'callable'
    can be scheduled and can also be 'wrapped' using `Clock.call`, which
    returns an object that schedules itself in the clock in the future once
    the wrapped object is called.

"""

from __future__ import absolute_import, division, print_function

from types import FunctionType, MethodType

from .Players import Player
from .Repeat import MethodCall
from .Patterns import asStream
from .TimeVar import TimeVar
from .Midi import MidiIn, MIDIDeviceNotFound
from .Utils import modi

from time import sleep, time, clock
from fractions import Fraction
from traceback import format_exc as error_stack

import sys
import threading
import inspect

class TempoClock(object):

    server = None

    def __init__(self, bpm=120.0, meter=(4,4)):

        # Flag this when done init
        self.__setup   = False

        # debug

        self.largest_sleep_time = 0
        self.last_block_dur = 0.0

        self.dtype=Fraction

        # Store time as a rational number
        
        self.time = self.dtype(0)
        self.beat = self.dtype(0)
        self.start_time = self.dtype(time())

        # Don't start yet...
        self.ticking = False

        # Player Objects stored here
        self.playing = []

        # Store history of osc messages and functions in here
        self.history = History()

        # All other scheduled items go here
        self.items   = []

        # General set up
        self.bpm   = bpm
        self.meter = meter

        # Create the queue
        self.queue = Queue()
        self.current_block = None
        
        # Midi Clock In
        self.midi_clock = None

        # Can be configured
        self.latency    = 0.25
        self.nudge      = 0.0
        self.sleep_time = 0.0001

        # Debug
        self.debugging = False
        self.__setup   = True

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
        if attr == "bpm" and self.__setup:
            # Schedule for next bar (taking into account latency for any "listening" FoxDot clients)
            self.schedule(lambda *args, **kwargs: object.__setattr__(self, attr, value))
            # Notify listening clients -- future
            pass
        else:
            self.__dict__[attr] = value
        return

    def bar_length(self):
        """ Returns the length of a bar in terms of beats """
        return (float(self.meter[0]) / self.meter[1]) * 4

    def beat_dur(self, n=1):
        """ Returns the length of n beats in seconds """
        return 0 if n == 0 else (60.0 / self.get_bpm()) * n

    def seconds_to_beats(self, seconds):
        """ Returns the number of beats that occur in a time period  """
        return (self.get_bpm() / 60.0) * seconds

    def get_bpm(self):
        if isinstance(self.bpm, TimeVar):
            bpm_val = self.bpm.now(self.beat)
        elif self.midi_clock:
            bpm_val = self.midi_clock.bpm
        else:
            bpm_val = self.bpm
        return float(bpm_val)

    def get_latency(self):
        """ Returns self.latency (which is in seconds) as a fraction of a beat """
        return self.seconds_to_beats(self.latency)

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

    def set_time(self, beat):
        """ Set the clock time to 'beat' and update players in the clock """
        self.start_time = time()
        self.queue.clear()
        self.beat = beat
        self.time = time() - self.start_time
        for player in self.playing:
            player(count=True)
        return

    def true_now(self):
        """ Returns the *actual* elapsed time (in beats) when adjusting for latency etc """
        # Get number of seconds elapsed
        now = self.dtype(((time() - self.start_time) - self.latency) + self.nudge)
        # Increment the beat counter
        self.beat += (now - self.time) * (self.dtype(self.get_bpm()) / 60)
        # Store time
        self.time  = now
        return self.beat

    def now(self):
        """ Returns the total elapsed time (in beats as opposed to seconds) """
        if not self.ticking:
            self.beat = self.true_now()
        return self.beat + self.beat_dur(self.latency)

    def osc_message_time(self):
        """ Returns the true time that an osc message should be run i.e. now + latency """
        return time() + self.latency - self.nudge
        
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

        # Set the time to "activate" messages on SC

        block.time = self.osc_message_time()

        for item in block:

            if not block.called(item):

                try:

                    block.call(item)

                except SystemExit:

                    sys.exit()

                except:

                    print(error_stack())

        # Send all the message to supercollider together

        block.send_osc_messages()

        # Store the osc messages

        self.history.add(block.beat, block.osc_messages)

        return

    def run(self):
        """ Main loop """
        
        self.ticking = True

        while self.ticking:

            beat = self.true_now() # get current time

            next_event = self.queue.next()

            if beat >= next_event:

                self.current_block = self.queue.pop()

                if len(self.current_block):

                    threading.Thread(target=self.__run_block, args=(self.current_block,)).start()

            # If using a midi-clock, update the values

            if self.midi_clock is not None:

                self.midi_clock.update()

            if self.sleep_time > 0:

                sleep(self.sleep_time)

        return


    def schedule(self, obj, beat=None, args=(), kwargs={}):
        """ TempoClock.schedule(callable, beat=None)
            Add a player / event to the queue """

        # Make sure the object can actually be called

        try:

            assert callable(obj)

        except AssertionError:

            raise ScheduleError(obj)

        # Start the clock ticking if not already

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

        self.queue.add(obj, beat, args, kwargs)

        return

    def next_bar(self):
        """ Returns the beat value for the start of the next bar """
        beat = self.now()
        return beat + (self.meter[0] - (beat % self.meter[0]))

    def next_event(self):
        """ Returns the beat index for the next event to be called """
        return self.queue[-1][1]

    def call(self, obj, dur, args=()):
        """ Returns a 'schedulable' wrapper for any callable object """
        return Wrapper(self, obj, dur, args)

    def players(self, exclude=[]):
        return [p for p in self.playing if p not in exclude]

    # Every n beats, do...

    def every(self, n, cmd, args=()):
        def event(f, n, args):
            f(*args)
            self.schedule(event, self.now() + n, (f, n, args))
            return
        self.schedule(event, self.now() + n, args=(cmd, n, args))
        return

    def stop(self):
        self.ticking = False
        self.clear()
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

        return

#####

class Queue(object):
    def __init__(self):
        self.data = []

    def __repr__(self):
        return "\n".join([str(item) for item in self.data]) if len(self.data) > 0 else "[]"

    def add(self, item, beat, args=(), kwargs={}):
        """ Adds a callable object to the queue at a specified beat, args and kwargs for the
            callable object must be in a list and dict.
        """
        
        # item must be callable to be schedule, so check args and kwargs are appropriate for it

        try:

            function = inspect.getargspec(item)

        except TypeError:

            function = inspect.getargspec(item.__call__)

        # If the item can't take arbitrary keywords, check any kwargs are valid

        if function.keywords is None: 

            for key in list(kwargs.keys()):

                if key not in function.args:

                    del kwargs[key]

        # If the new event is before the next scheduled event,
        # move it to the 'front' of the queue

        if beat < self.next():

            self.data.append(QueueItem(item, beat, args, kwargs))

            block = self.data[-1]

        else:

            # If the event is after the next scheduled event, work
            # out its position in the queue

            # need to be careful in case self.data changes size
            
            for block in self.data:

                # If another event is happening at the same time, schedule together

                if beat == block.beat:

                    block.add(item, args, kwargs)                    

                    break

                # If the event is later than the next event, schedule it here

                if beat > block.beat:

                    try:

                        i = self.data.index(block)

                    except ValueError:

                        i = 0

                    self.data.insert(i, QueueItem(item, beat, args, kwargs))

                    block = self.data[i]

                    break

        # Tell any players about what queue item they are in

        if hasattr(item, "queue_block"):

            item.queue_block = block

        return

    def clear(self):
        while len(self.data):
            del self.data[-1]
        return

    def pop(self):
        return self.data.pop() if len(self.data) > 0 else list()

    def next(self):
        if len(self.data) > 0:
            try:
                return self.data[-1].beat
            except IndexError:
                pass
        return sys.maxsize
            
from types import FunctionType
class QueueItem(object):
    priority_levels = [
                        lambda x: type(x) == FunctionType,   # Any functions are called first
                        lambda x: isinstance(x, MethodCall), # Then scheduled player methods
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
        self.time = 0
        self.add(obj, args, kwargs)
        
    def __repr__(self):
        return "{}: {}".format(self.beat, self.players())
    
    def add(self, obj, args=(), kwargs={}):
        """ Adds a callable object to the QueueItem """

        q_obj = QueueObj(obj, args, kwargs)

        for i, level in enumerate(self.priority_levels):

            if level(obj):

                self.events[i].append(q_obj)

                break
        return

    def __call__(self):
        self.send_osc_messages()

    def send_osc_messages(self):
        """ Sends all compiled osc messages to the SuperCollider server """
        for msg in self.osc_messages:
            if msg.address == "/foxdot_midi":
                self.server.sclang.send(msg)
            else:
                self.server.client.send(msg)        
        return

    def called(self, item):
        """ Returns True if the item is in this QueueItem and has already been called """
        return item in self.called_events

    def call(self, item, caller = None):
        """ Calls all items in queue slot """
        # TODO -> Make more efficient -> and understand what is going on
        
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
            if event == key:
                return event # Possible need to be key.obj?

    def players(self):
        return [item for level in self.events[1:3] for item in level]

    def __iter__(self):
        return (item for level in self.events for item in level)

    def __len__(self):
        return sum([len(level) for level in self.events])

    def objects(self):
        return [item.obj for level in self.events for item in level]
        

class QueueObj(object):
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

class History(object):
    """
    Stores osc messages send from the TempoClock so that if the
    Clock is reveresed we can just send the osc messages already sent

    """
    def __init__(self):
        self.data = []
    def add(self, beat, osc_messages):
        self.data.append(osc_messages)

##import Code
##
##class Wrapper(Code.LiveObject):
##    
##    def __init__(self, metro, obj, dur, args=()):
##        self.args  = asStream(args)
##        self.obj   = obj
##        self.step  = dur
##        self.metro = metro
##        self.n     = 0
##        self.s     = self.obj.__class__.__name__
##
##    def __str__(self):
##        return "<Scheduled Call '%s'>" % self.s
##
##    def __repr__(self):
##        return  str(self)
##
##    def __call__(self):
##        """ Call the wrapped object and re-schedule """
##        args = modi(self.args, self.n)
##        try:
##            self.obj.__call__(*args)
##        except:
##            self.obj.__call__(args)
##        Code.LiveObject.__call__(self)

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


class ScheduleError(Exception):
    def __init__(self, item):
        self.type = str(type(item))[1:-1]
    def __str__(self):
        return "Could not schedule object of {}".format(self.type)
