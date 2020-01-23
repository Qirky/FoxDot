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
from .ServerManager import TempoClient, ServerManager, RequestTimeout
from .Settings import CPU_USAGE, CLOCK_LATENCY

import time
from fractions import Fraction
from traceback import format_exc as error_stack

import sys
import threading
import inspect

class TempoClock(object):

    tempo_server = None
    tempo_client = None
    waiting_for_sync = False

    def __init__(self, bpm=120.0, meter=(4,4)):

        # Flag this when done init
        self.__setup   = False

        # debug information

        self.largest_sleep_time = 0
        self.last_block_dur = 0.0

        # Storing time as a float 

        self.dtype=float
        
        self.beat       = self.dtype(0) # Beats elapsed
        self.last_now_call = self.dtype(0)

        self.ticking = True #?? 

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

        # EspGrid sync
        self.espgrid = None

        # Flag for next_bar wrapper
        self.now_flag  = False

        # Can be configured
        self.latency_values = [0.25, 0.5, 0.75]
        self.latency    = 0.25 # Time between starting processing osc messages and sending to server
        self.nudge      = 0.0  # If you want to synchronise with something external, adjust the nudge
        self.hard_nudge = 0.0

        self.bpm_start_time = time.time()
        self.bpm_start_beat = 0

        # The duration to sleep while continually looping
        self.sleep_values = [0.01, 0.001, 0.0001]
        self.sleep_time = self.sleep_values[CPU_USAGE]
        self.midi_nudge = 0

        # Debug
        self.debugging = False
        self.__setup   = True

        # If one object is going to played
        self.solo = SoloPlayer()

        self.thread = threading.Thread(target=self.run)

    def sync_to_espgrid(self, host="localhost", port=5510):
        """ Connects to an EspGrid instance """
        from .EspGrid import EspGrid
        self.espgrid = EspGrid((host, port))
        try:
            tempo = self.espgrid.get_tempo()
        except RequestTimeout:
            err = "Unable to reach EspGrid. Make sure the application is running and try again."
            raise RequestTimeout(err)
        
        self.espgrid.set_clock_mode(2)
        self.schedule(lambda: self._espgrid_update_tempo(True))
        # self._espgrid_update_tempo(True) # could schedule this for next bar?
        return

    def _espgrid_update_tempo(self, force=False):
        """ Retrieves the current tempo from EspGrid and updates internal values """

        data = self.espgrid.get_tempo()

        # If the tempo hasn't been started, start it here and get updated data
        
        if data[0] == 0:
            self.espgrid.start_tempo()
            data = self.espgrid.get_tempo()
        
        if force or (data[1] != self.bpm):
            self.bpm_start_time = float("{}.{}".format(data[2], data[3]))
            self.bpm_start_beat = data[4]
            object.__setattr__(self, "bpm", self._convert_json_bpm(data[1]))

        # self.schedule(self._espgrid_update_tempo)
        self.schedule(self._espgrid_update_tempo, int(self.now() + 1))
        
        return

    def reset(self):
        """ Deprecated """
        self.time = self.dtype(0)
        self.beat = self.dtype(0)
        self.start_time = time.time()
        return

    @classmethod
    def set_server(cls, server):
        """ Sets the destination for OSC messages being compiled (the server is also the class
            that compiles them) via objects in the clock. Should be an instance of ServerManager -
            see ServerManager.py for more. """
        assert isinstance(server, ServerManager)
        cls.server = server
        return

    @classmethod
    def add_method(cls, func):
        setattr(cls, func.__name__, func)

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

    def flag_wait_for_sync(self, value):
        self.waiting_for_sync = bool(value)

    def connect(self, ip_address, port=57999):
        try:
            self.tempo_client = TempoClient(self)
            self.tempo_client.connect(ip_address, port)
            self.tempo_client.send(["request"])
            self.flag_wait_for_sync(True)
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

    def update_tempo_now(self, bpm):
        """ emergency override for updating tempo"""
        self.last_now_call = self.bpm_start_time = time.time()
        self.bpm_start_beat = self.now()
        object.__setattr__(self, "bpm", self._convert_json_bpm(bpm))
        # self.update_network_tempo(bpm, start_beat, start_time) -- updates at the bar...
        return

    def set_tempo(self, bpm, override=False):
        """ Short-hand for update_tempo and update_tempo_now """
        return self.update_tempo_now(bpm) if override else self.update_tempo(bpm)

    def update_tempo(self, bpm):
        """ Schedules the bpm change at the next bar, returns the beat and start time of the next change """

        try:

            assert bpm > 0, "Tempo must be a positive number"

        except AssertionError as err:

            raise(ValueError(err))

        next_bar = self.next_bar()

        bpm_start_time = self.get_time_at_beat(next_bar)
        bpm_start_beat = next_bar

        def func():
            
            if self.espgrid is not None:

                self.espgrid.set_tempo(bpm)

            else:

                object.__setattr__(self, "bpm", self._convert_json_bpm(bpm))
                self.last_now_call = self.bpm_start_time = bpm_start_time
                self.bpm_start_beat = bpm_start_beat

        # Give next bar value to bpm_start_beat
        self.schedule(func, next_bar, is_priority=True)

        return bpm_start_beat, bpm_start_time

    def update_tempo_from_connection(self, bpm, bpm_start_beat, bpm_start_time, schedule_now=False):
        """ Sets the bpm externally from another connected instance of FoxDot """

        def func():
            self.last_now_call = self.bpm_start_time = self.get_time_at_beat(bpm_start_beat)
            self.bpm_start_beat = bpm_start_beat
            object.__setattr__(self, "bpm", self._convert_json_bpm(bpm))
        
        # Might be changing immediately
        if schedule_now:
        
            func()
        
        else:
        
            self.schedule(func, is_priority=True)
        
        return 

    def update_network_tempo(self, bpm, start_beat, start_time):
        """ Updates connected FoxDot instances (client or servers) tempi """

        json_value = self._convert_bpm_json(bpm)

        # If this is a client, send info to server

        if self.tempo_client is not None:
        
            self.tempo_client.update_tempo(json_value, start_beat, start_time)

        # If this is a server, send info to clients
        
        if self.tempo_server is not None:
        
            self.tempo_server.update_tempo(None, json_value, start_beat, start_time)

        return


    def swing(self, amount=0.1):
        """ Sets the nudge attribute to var([0, amount * (self.bpm / 120)],1/2)"""
        self.nudge = TimeVar([0, amount * (self.bpm / 120)], 1/2) if amount != 0 else 0
        return

    def set_cpu_usage(self, value):
        """ Sets the `sleep_time` attribute to values based on desired high/low/medium cpu usage """
        assert 0 <= value <= 2
        self.sleep_time = self.sleep_values[value]
        return

    def set_latency(self, value):
        """ Sets the `latency` attribute to values based on desired high/low/medium latency """
        assert 0 <= value <= 2
        self.latency = self.latency_values[value]
        return

    def __setattr__(self, attr, value):
        if attr == "bpm" and self.__setup:

            # If connected to EspGrid, just update that

            # if self.espgrid is not None:

            #     self.espgrid.set_tempo(value)

            # else:

            #     # Schedule for next bar

            #     start_beat, start_time = self.update_tempo(value)

            #     # Checks if any peers are connected and updates them also

            #     self.update_network_tempo(value, start_beat, start_time)

            # Schedule for next bar

            start_beat, start_time = self.update_tempo(value)

            # Checks if any peers are connected and updates them also

            self.update_network_tempo(value, start_beat, start_time)

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

    def get_elapsed_beats_from_last_bpm_change(self):
        """ Returns the number of beats that *should* have elapsed since the last tempo change """
        return float(self.get_elapsed_seconds_from_last_bpm_change() * (self.get_bpm() / 60))

    def get_elapsed_seconds_from_last_bpm_change(self):
        """ Returns the time since the last change in bpm """
        return self.get_time() - self.bpm_start_time

    def get_time(self):
        """ Returns current machine clock time with nudges values added """
        return time.time() + float(self.nudge) + float(self.hard_nudge)

    def get_time_at_beat(self, beat):
        """ Returns the time that the local computer's clock will be at 'beat' value """
        if isinstance(self.bpm, TimeVar):
            t = self.get_time() + self.beat_dur(beat - self.now())        
        else:
            t = self.bpm_start_time + self.beat_dur(beat - self.bpm_start_beat) 
        return t

    def sync_to_midi(self, port=0, sync=True):
        """ If there is an available midi-in device sending MIDI Clock messages,
            this attempts to follow the tempo of the device. Requies rtmidi """
        try:
            if sync:
                self.midi_clock = MidiIn(port)
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
        self.start_time = time.time()
        self.queue.clear()
        self.beat = beat
        self.bpm_start_beat = beat
        self.bpm_start_time = self.start_time
        # self.time = time() - self.start_time
        for player in self.playing:
            player(count=True)
        return

    def calculate_nudge(self, time1, time2, latency):
        """ Approximates the nudge value of this TempoClock based on the machine time.time()
            value from another machine and the latency between them """
        # self.hard_nudge = time2 - (time1 + latency)
        self.hard_nudge = time1 - time2 - latency
        return

    def _convert_bpm_json(self, bpm):
        if isinstance(bpm, (int, float)):
            return float(bpm)
        elif isinstance(bpm, TimeVar):
            return bpm.json_value()

    def json_bpm(self):
        """ Returns the bpm in a data type that can be sent over json"""
        return self._convert_bpm_json(self.bpm)

    def get_sync_info(self):
        """ Returns information for synchronisation across multiple FoxDot instances. To be 
            stored as a JSON object with a "sync" header """

        data = {
            "sync" : {
                "bpm_start_time" : float(self.bpm_start_time),
                "bpm_start_beat" : float(self.bpm_start_beat),
                "bpm"            : self.json_bpm(),
            }
        }

        return data

    def _now(self):
        """ If the bpm is an int or float, use time since the last bpm change to calculate what the current beat is. 
            If the bpm is a TimeVar, increase the beat counter by time since last call to _now()"""
        if isinstance(self.bpm, (int, float)):
            self.beat = self.bpm_start_beat + self.get_elapsed_beats_from_last_bpm_change()
        else:
            now = self.get_time()
            self.beat += (now - self.last_now_call) * (self.get_bpm() / 60)
            self.last_now_call = now
        return self.beat

    def now(self):
        """ Returns the total elapsed time (in beats as opposed to seconds) """
        if self.ticking is False: # Get the time w/o latency if not ticking
            self.beat = self._now()
        return float(self.beat)

    def mod(self, beat, t=0):
        """ Returns the next time at which `Clock.now() % beat` will equal `t` """
        n = self.now() // beat
        return (n + 1) * beat + t 

    def osc_message_time(self):
        """ Returns the true time that an osc message should be run i.e. now + latency """
        return time.time() + self.latency
        
    def start(self):
        """ Starts the clock thread """ 
        self.thread.daemon = True
        self.thread.start()
        return

    def _adjust_hard_nudge(self):
        """ Checks for any drift between the current beat value and the value
            expected based on time elapsed and adjusts the hard_nudge value accordingly """
        
        beats_elapsed = int(self.now()) - self.bpm_start_beat
        expected_beat = self.get_elapsed_beats_from_last_bpm_change()

        # Dont adjust nudge on first bar of tempo change

        if beats_elapsed > 0:

            # Account for nudge in the drift

            self.drift  = self.beat_dur(expected_beat - beats_elapsed) - self.nudge

            if abs(self.drift) > 0.001: # value could be reworked / not hard coded

                self.hard_nudge -= self.drift

        return self._schedule_adjust_hard_nudge()

    def _schedule_adjust_hard_nudge(self):
        """ Start recursive call to adjust hard-nudge values """
        return self.schedule(self._adjust_hard_nudge)

    def __run_block(self, block, beat):
        """ Private method for calling all the items in the queue block.
            This means the clock can still 'tick' while a large number of
            events are activated  """

        # Set the time to "activate" messages on - adjust in case the block is activated late

        # `beat` is the actual beat this is happening, `block.beat` is the desired time. Adjust
        # the osc_message_time accordingly if this is being called late

        block.time = self.osc_message_time() - self.beat_dur(float(beat) - block.beat)

        for item in block:

            # The item might get called by another item in the queue block

            output = None

            if item.called is False:

                try:

                    output = item.__call__()

                except SystemExit:

                    sys.exit()

                except:

                    print(error_stack())

                # TODO: Get OSC message from the call, and add to list?

        # Send all the message to supercollider together

        block.send_osc_messages()

        # Store the osc messages -- future idea

        # self.history.add(block.beat, block.osc_messages)

        return

    def run(self):
        """ Main loop """
        
        self.ticking = True

        self.polled = False

        while self.ticking:

            beat = self._now() # get current time

            if self.queue.after_next_event(beat):

                self.current_block = self.queue.pop()

                # Do the work in a thread

                if len(self.current_block):

                    threading.Thread(target=self.__run_block, args=(self.current_block, beat)).start()

            # If using a midi-clock, update the values

            # if self.midi_clock is not None:

                # self.midi_clock.update()

            # if using espgrid

            if self.sleep_time > 0:

                time.sleep(self.sleep_time)

        return

    def schedule(self, obj, beat=None, args=(), kwargs={}, is_priority=False):
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

        self.queue.add(obj, beat, args, kwargs, is_priority)

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

        # for item in self.items:

        #     if hasattr(item, 'stop'):

        #         item.stop()
        
        self.playing = []

        if self.espgrid is not None:

            self.schedule(self._espgrid_update_tempo)
        
        return

#####

class Queue(object):
    def __init__(self, parent):
        self.data = []
        self.parent = parent

    def __repr__(self):
        return "\n".join([str(item) for item in self.data]) if len(self.data) > 0 else "[]"

    def add(self, item, beat, args=(), kwargs={}, is_priority=False):
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

        if self.before_next_event(beat):

            self.data.append(QueueBlock(self, item, beat, args, kwargs, is_priority))

            block = self.data[-1]

        else:

            # If the event is after the next scheduled event, work
            # out its position in the queue

            # need to be careful in case self.data changes size
            
            for block in self.data:

                # If another event is happening at the same time, schedule together

                if beat == block.beat:

                    block.add(item, args, kwargs, is_priority)

                    break

                # If the event is later than the next event, schedule it here

                if beat > block.beat:

                    try:

                        i = self.data.index(block)

                    except ValueError:

                        i = 0

                    self.data.insert(i, QueueBlock(self, item, beat, args, kwargs, is_priority))

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

    def before_next_event(self, beat):
        try:
            return beat < self.data[-1].beat
        except IndexError:
            return True

    def after_next_event(self, beat):
        try:
            return beat >= self.data[-1].beat
        except IndexError:
            return False

    def get_server(self):
        """ Returns the `ServerManager` instanced used by this block's parent clock """
        return self.parent.server

    def get_clock(self):
        return self.parent
            
from types import FunctionType
class QueueBlock(object):
    priority_levels = [
                        lambda x: type(x) in (FunctionType, MethodType),   # Any functions are called first
                        lambda x: isinstance(x, MethodCall), # Then scheduled player methods
                        lambda x: isinstance(x, Player),     # Then players themselves
                        lambda x: True                       # And anything else
                      ]
                       
    def __init__(self, parent, obj, t, args=(), kwargs={}, is_priority=False): # Why am I forcing an obj?

        self.events         = [ [] for lvl in self.priority_levels ]
        self.called_events  = []
        self.called_objects = []
        self.items = {}

        self.osc_messages   = []

        self.parent = parent
        self.server = self.parent.get_server()
        self.metro  = self.parent.get_clock()

        self.beat = t
        self.time = 0
        self.add(obj, args, kwargs, is_priority)

    @classmethod
    def set_server(cls, server):
        cls.server = server # osc server

    def start_server(self, serv):
        self.tempo_server = serv(self)
        return
        
    def __repr__(self):
        return "{}: {}".format(self.beat, self.players())
    
    def add(self, obj, args=(), kwargs={}, is_priority=False):
        """ Adds a callable object to the QueueBlock """

        q_obj = QueueObj(obj, args, kwargs)

        for i, in_level in enumerate(self.priority_levels):

            if in_level(obj):

                # Put at the front if labelled as priority

                if is_priority:

                    self.events[i].insert(0, q_obj)

                else:

                    self.events[i].append(q_obj)

                self.items[q_obj.obj] = q_obj # store the wrapped object as an identifer

                break
        return

    def __call__(self):
        """ Calls self.osc_messages() """
        self.send_osc_messages()

    def append_osc_message(self, message):
        """ Adds an OSC bundle if the timetag is not in the past """
        if message.timetag > self.metro.get_time():
            self.osc_messages.append(message)
        return

    def send_osc_messages(self):
        """ Sends all compiled osc messages to the SuperCollider server """
        return list(map(self.server.sendOSC, self.osc_messages))

    def players(self):
        return [item for level in self.events[1:3] for item in level]

    def all_items(self):
        return [item for level in self.events for item in level]

    def __getitem__(self, key): # could this use hashing with Player objects?
        return self.items[key]

    def __iter__(self):
        return (item for level in self.events for item in level)

    def __len__(self):
        return sum([len(level) for level in self.events])

    def __contains__(self, other):
        return other in self.items

    def objects(self):
        return [item.obj for level in self.events for item in level]
        

class QueueObj(object):
    """ Class representing each item in a `QueueBlock` instance """
    def __init__(self, obj, args=(), kwargs={}):
        self.obj = obj
        self.args = args
        self.kwargs = kwargs
        self.called = False # flag to True when called by the block
    def __eq__(self, other):
        return other == self.obj
    def __ne__(self, other):
        return other != self.obj
    def __repr__(self):
        return repr(self.obj)
    def __call__(self):
        value = self.obj.__call__(*self.args, **self.kwargs)
        self.called = True
        return value

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
