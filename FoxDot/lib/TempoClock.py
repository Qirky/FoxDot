"""
    Clock management for scheduling notes and functions. Anything 'callable', such as a function
    or instance with a `__call__` method, can be scheduled. An instance of `TempoClock` is created
    when FoxDot started up called `Clock`, which is used by `Player` instances to schedule musical
    events. 

    The `TempoClock` is also responsible for sending the osc messages to SuperCollider. It contains
    a queue of event blocks, instances of the `QueueBlock` class, which themselves contain queue
    items, instances of the `QueueObj` class, which themseles contain the actual object or function
    to be called. The `TempoClock` is continually running and checks if any queue block should 
    be activated. A queue block has a "beat" value for which its contents should be activated. To make
    sure that events happen on time, the `TempoClock` will begin processing the contents 0.25
    seconds before it is *actually* meant to happen in case there is a large amount to process.  When 
    a queue block is activated, a new thread is created to process all of the callable objects it
    contains. If it calls a `Player` object, the queue block keeps track of the OSC messages generated 
    until all `Player` objects in the block have been called. At this point the thread is told to
    sleep until the remainder of the 0.25 seconds has passed. This value is stored in `Clock.latency`
    and is adjustable. If you find that there is a noticeable jitter between events, i.e. irregular
    beat lengths, you can increase the latency by simply evaluating the following in FoxDot:

        Clock.latency = 0.5

    To stop the clock from scheduling further events, use the `Clock.clear()` method, which is
    bound to the shortcut key, `Ctrl+.`. You can schedule non-player objects in the clock by
    using `Clock.schedule(func, beat, args, kwargs)`. By default `beat` is set to the next
    bar in the clock, but you use `Clock.now() + n` or `Clock.next_bar() + n` to schedule a function
    in the future at a specific time. 

    To change the tempo of the clock, just set the bpm attribute using `Clock.bpm=val`. The change
    in tempo will occur at the start of the next bar so be careful if you schedule this action within
    a function like this:

        def myFunc():
            print("bpm change!")
            Clock.bpm+=50

    This will print the string `"bpm change"` at the next bar and change the bpm value at the
    start of the *following* bar. The reason for this is to make it easier for calculating
    currently clock times when using a `TimeVar` instance (See docs on TimeVar.py) as a tempo.

    You can change the clock's time signature as you would change the tempo by setting the
    `meter` attribute to a tuple with two values. So for 3/4 time you would use the follwing
    code:

        Clock.meter = (3,4)

"""

from __future__ import absolute_import, division, print_function

from types import FunctionType, MethodType

from .Players import Player
from .Repeat import MethodCall
from .Patterns import asStream
from .TimeVar import TimeVar
from .Midi import MidiIn, MIDIDeviceNotFound
from .Utils import modi
from .ServerManager import TempoClient, ServerManager

from time import sleep, time, clock
from fractions import Fraction
from traceback import format_exc as error_stack

import sys
import threading
import inspect

class TempoClock(object):

    tempo_server = None
    tempo_client = None

    def __init__(self, bpm=120.0, meter=(4,4)):

        # Flag this when done init
        self.__setup   = False

        # debug

        self.largest_sleep_time = 0
        self.last_block_dur = 0.0

        self.dtype=Fraction

        # Store time as a rational number
        
        self.time       = self.dtype(0) # Seconds elsapsed
        self.beat       = self.dtype(0) # Beats elapsed
        self.start_time = self.dtype(time()) # could set to 0?

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
        self.queue = Queue(self)
        self.current_block = None
        
        # Midi Clock In
        self.midi_clock = None

        # Can be configured
        self.latency    = 0.25 # Time between starting processing osc messages and sending to server
        self.nudge      = 0.0  # If you want to synchronise with something external, adjust the nudge
        self.hard_nudge = 0.0
        self.sleep_time = 0.0001 # The duration to sleep while continually looping
        self.midi_nudge = 0

        # Debug
        self.debugging = False
        self.__setup   = True

        # If one object is going to played
        self.solo = SoloPlayer()

    @classmethod
    def set_server(cls, server):
        """ Sets the destination for OSC messages being compiled (the server is also the class
            that compiles them) via objects in the clock. Should be an instance of ServerManager -
            see ServerManager.py for more. """
        assert isinstance(server, ServerManager)
        cls.server = server
        return

    def start_tempo_server(self, serv, **kwargs):
        """ Starts listening for FoxDot clients connecting over a network. This uses
            a TempoClient instance from ServerManager.py """
        self.tempo_server = serv(self, **kwargs)
        self.tempo_server.start()
        return

    def kill_tempo_server(self):
        """ Kills the tempo server """
        if self.tempo_server is not None:
            self.tempo_server.kill()
        return

    def connect(self, ip_address, port=57999):
        try:
            self.tempo_client = TempoClient(self)
            self.tempo_client.connect(ip_address, port)
            self.tempo_client.send({"request" : ["bpm", "start_time", "beat", "time"]})
        except ConnectionRefusedError as e:
            print(e)
        pass

    def kill_tempo_client(self):
        if self.tempo_client is not None:
            self.tempo_client.kill()
        return

    def __str__(self):
        return str(self.queue)

    def __iter__(self):
        for x in self.queue:
            yield x

    def __len__(self):
        return len(self.queue)

    def __contains__(self, item):
        return item in self.items

    def update_tempo(self, bpm):
        """ Schedules the bpm change at the next bar """
        return self.schedule(lambda *args, **kwargs: object.__setattr__(self, "bpm", bpm))

    def __setattr__(self, attr, value):
        if attr == "bpm" and self.__setup:

            # Schedule for next bar (taking into account latency for any "listening" FoxDot clients)

            self.update_tempo(value)

            # Notify listening clients
            if self.tempo_client is not None:
            
                self.tempo_client.update_tempo(value)
            
            if self.tempo_server is not None:
            
                self.tempo_server.update_tempo(value)

        elif attr == "midi_nudge" and self.__setup:

            # Adjust nudge for midi devices

            self.server.set_midi_nudge(value)

            object.__setattr__(self, "midi_nudge", value)
                
        else:
            self.__dict__[attr] = value
        return

    def bar_length(self):
        """ Returns the length of a bar in terms of beats """
        return (float(self.meter[0]) / self.meter[1]) * 4

    def bars(self, n=1):
        """ Returns the number of beats in 'n' bars """
        return self.bar_length() * n

    def beat_dur(self, n=1):
        """ Returns the length of n beats in seconds """
        return 0 if n == 0 else (60.0 / self.get_bpm()) * n

    def beats_to_seconds(self, beats):
        return self.beat_dur(beats)

    def seconds_to_beats(self, seconds):
        """ Returns the number of beats that occur in a time period  """
        return (self.get_bpm() / 60.0) * seconds

    def get_bpm(self):
        """ Returns the current beats per minute as a floating point number """
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
        """ Toggles debugging information printing to console """
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

    def calculate_nudge(self, time1, time2, latency):
        """ Approximates the nudge value of this TempoClock based on the machine time.time()
            value from another machine and the latency between them """
        self.hard_nudge = time2 - (time1 + latency)
        return

    def get_sync_info(self):
        """ Returns a serialisable value for Fraction values etc"""

        data = {
            "sync" : {
                "start_time" : (self.start_time.numerator, self.start_time.denominator),
                "bpm"        : float(self.bpm), # TODO: serialise timevar etc
                "beat"       : (self.beat.numerator, self.beat.denominator),
                "time"       : (self.time.numerator, self.time.denominator)
            }
        }

        return data


    def set_attr(self, key, value):
        """ Sets the value of self.key when key is a string """

        if key == "bpm":

            self.bpm = value

        else:

            setattr(self, key, Fraction(value[0], value[1]))

        return

    def get_elapsed_sec(self):
        return self.dtype( time() - (self.start_time + (self.nudge + self.hard_nudge)) - self.latency )

    def true_now(self):
        """ Returns the *actual* elapsed time (in beats) when adjusting for latency etc """
        # Get number of seconds elapsed
        now = self.get_elapsed_sec()
        # Increment the beat counter
        self.beat += (now - self.time) * (self.dtype(self.get_bpm()) / 60)
        # Store time
        self.time  = now
        return self.beat

    def now(self):
        """ Returns the total elapsed time (in beats as opposed to seconds) """
        if self.ticking is False: # Get the time w/o latency if not ticking
            self.beat = self.true_now()
        return self.beat + self.beat_dur(self.latency)

    def osc_message_time(self):
        """ Returns the true time that an osc message should be run i.e. now + latency """
        return time() + self.latency
        
    def start(self):
        """ Starts the clock thread """
        main = threading.Thread(target=self.run)
        main.daemon = True
        main.start()
        return

    def __run_block(self, block, time):
        """ Private method for calling all the items in the queue block.
            This means the clock can still 'tick' while a large number of
            events are activated  """

        # Set the time to "activate" messages on - adjust in case the block is activated late

        block.time = self.osc_message_time() - self.beat_dur(float(time) - block.beat)

        for item in block:

            # The item might get called by another item in the queue block

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

                    threading.Thread(target=self.__run_block, args=(self.current_block, beat)).start()

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

        # block.time = self.osc_message_accum

        return

    def future(self, dur, obj, args=(), kwargs={}):
        """ Add a player / event to the queue `dur` beats in the future """
        self.schedule(obj, self.now() + dur, args, kwargs)
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

    def players(self, ex=[]):
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
        self.kill_tempo_server()
        self.kill_tempo_client()
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

        for player in list(self.playing):

            player.kill()

        for item in self.items:

            if hasattr(item, 'stop'):

                item.stop()             
        
        self.playing = []
        self.ticking = False

        return

#####

class Queue(object):
    def __init__(self, parent):
        self.data = []
        self.parent = parent

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

            self.data.append(QueueBlock(self, item, beat, args, kwargs))

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

                    self.data.insert(i, QueueBlock(self, item, beat, args, kwargs))

                    block = self.data[i]

                    break

        # Tell any players about what queue item they are in

        if isinstance(item, Player):

            item.set_queue_block(block)

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

    def get_server(self):
        """ Returns the `ServerManager` instanced used by this block's parent clock """
        return self.parent.server

    def get_clock(self):
        return self.parent
            
from types import FunctionType
class QueueBlock(object):
    priority_levels = [
                        lambda x: type(x) == FunctionType,   # Any functions are called first
                        lambda x: isinstance(x, MethodCall), # Then scheduled player methods
                        lambda x: isinstance(x, Player),     # Then players themselves
                        lambda x: True                       # And anything else
                      ]
                       
    def __init__(self, parent, obj, t, args=(), kwargs={}):

        self.events         = [ [] for lvl in self.priority_levels ]
        self.called_events  = []
        self.called_objects = []

        self.osc_messages   = []

        self.parent = parent
        self.server = self.parent.get_server()
        self.metro  = self.parent.get_clock()

        self.beat = t
        self.time = 0
        self.add(obj, args, kwargs)

    @classmethod
    def set_server(cls, server):
        cls.server = server # osc server

    def start_server(self, serv):
        self.tempo_server = serv(self)
        return
        
    def __repr__(self):
        return "{}: {}".format(self.beat, self.players())
    
    def add(self, obj, args=(), kwargs={}):
        """ Adds a callable object to the QueueBlock """

        q_obj = QueueObj(obj, args, kwargs)

        for i, in_level in enumerate(self.priority_levels):

            if in_level(obj):

                self.events[i].append(q_obj)

                break
        return

    def __call__(self):
        """ Calls self.osc_messages() """
        self.send_osc_messages()

    def send_osc_messages(self):
        """ Sends all compiled osc messages to the SuperCollider server """
        for msg in self.osc_messages:
            self.server.sendOSC(msg)
        return

    def call(self, item, caller = None):
        """ Calls an item in queue slot """

        # This item (likely a Player) might be called by another Player

        if caller is not None:

            # Caller will call the actual object, get the queue_item

            item = self.get_queue_item(item)

        if item not in self.called_events:

            self.called_events.append(item)

            item()

        return

    # Remove duplication

    def already_called(self, obj):
        """ Returns True if the obj (not QueueItem) has been called """
        return self.get_queue_item(obj) in self.called_events

    def called(self, item):
        """ Returns True if the item is in this QueueBlock and has already been called """
        return item in self.called_events

    def get_queue_item(self, obj):
        for item in self:
            if item.obj == obj:
                return item
        else:
            raise ValueError("{} not found".format(key))

    def players(self):
        return [item for level in self.events[1:3] for item in level]

    def all_items(self):
        return [item for level in self.events for item in level]

    def __getitem__(self, key):
        for event in self:
            if event == key:
                return event # Possible need to be key.obj?
        else:
            raise ValueError("{} not found".format(key))

    def __iter__(self):
        return (item for level in self.events for item in level)

    def __len__(self):
        return sum([len(level) for level in self.events])

    def __contains__(self, other):
        return other in self.objects()

    def objects(self):
        return [item.obj for level in self.events for item in level]
        

class QueueObj(object):
    """ Class representing each item in a `QueueBlock` instance """
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

from . import Code

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


class ScheduleError(Exception):
    def __init__(self, item):
        self.type = str(type(item))[1:-1]
    def __str__(self):
        return "Could not schedule object of {}".format(self.type)
