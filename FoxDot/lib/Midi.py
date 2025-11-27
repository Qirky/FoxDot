""" Module for converting handling MIDI in/out and functions relating to MIDI pitch calculation. """

from __future__ import absolute_import, division, print_function

from collections import defaultdict
from dataclasses import dataclass, field
from itertools import chain, cycle
from traceback import format_exc
from typing import Callable, overload
from uuid import uuid4

try:
    import rtmidi
    from rtmidi import midiconstants
    from rtmidi.midiconstants import (
        NOTE_OFF, TIMING_CLOCK, SONG_POSITION_POINTER, SONG_START, SONG_STOP
    )
    from rtmidi.midiutil import list_input_ports, open_midiinput

except ImportError as _err:
    pass

from .SCLang import SynthDefProxy
from .TimeVar import TimeVar, var


class MidiInputHandler(object):

    """Midi Handler CallBack Function"""

    def __init__(self, midi_ctrl):

        self.midi_ctrl = midi_ctrl
        self.bpm_group = []
        self.played = False

    def __call__(self, event, data=None):

        datatype, delta = event

        self.midi_ctrl.delta += delta
        
        if TIMING_CLOCK in datatype and not self.played:

            self.midi_ctrl.pulse += 1
            

            if self.midi_ctrl.pulse == self.midi_ctrl.ppqn:

                t_master = 60.0
                
                self.midi_ctrl.bpm = round(60.0 / self.midi_ctrl.delta,0)

                self.midi_ctrl.pulse = 0
                self.midi_ctrl.delta = 0.0

                #print("BPM : " + repr(self.midi_ctrl.bpm))
            
class MidiIn:
    metro = None
    def __init__(self, port_id=0):
        """ Class for listening for MIDI clock messages
            from a midi device """
        try:

            self.device = rtmidi.MidiIn()

        except NameError as _err:

            raise ImportError(_err)

        self.available_ports = self.device.get_ports()

        if not self.available_ports:

            raise MIDIDeviceNotFound

        else:

            print("MidiIn: Connecting to " + self.available_ports[port_id])

        self.device.open_port(port_id)
        self.device.ignore_types(timing=False)


        self.pulse = 0
        self.delta = 0.0
        self.bpm   = 120.0
        self.ppqn  = 24
        self.beat  = 0

        self.device.set_callback(MidiInputHandler(self))

    @classmethod
    def set_clock(cls, tempo_clock):
        cls.metro = tempo_clock
        return

    def close(self):
        """ Closes the active port """
        self.device.close_port()
        return


class MidiOut(SynthDefProxy):
    """ SynthDef proxy for sending midi message via supercollider """
    def __init__(self, degree=0, **kwargs):
        SynthDefProxy.__init__(self, self.__class__.__name__, degree, kwargs)

midi = MidiOut # experimental alias

# Midi information exceptions

class MIDIDeviceNotFound(Exception):
    def __str__(self):
        return self.__class__.__name__ + " Error"

class rtMidiNotFound(Exception):
    def __str__(self):
        return self.__class__.__name__ + ": Module 'rtmidi' not found"


Handler = Callable[['CC.Msg'], None]


@dataclass
class Controler:
    """Controler handler."""

    cc: 'CC'
    number: str = 'all'

    def __call__(self, func) -> Handler:
        """Control functions.

        Example:
            >>> @Controler(cc, 1)
            ... def _(msg: cc.Msg):
            ...     print(msg)

            or

            >>> @cc(1)
            ... def _(msg: cc.Msg):
            ...     print(msg)
        """
        return self.cc.add_handler(str(self.number), func, unique=True)

    def switch(self, *options) -> TimeVar:
        """Switch cycle timevar.

        Useful for use as buttons.

        Example:
            >>> d1 >> play('x.', amp=cc(1).switch(1,0))
        """
        values = cycle(options)
        value = next(values)

        def _get(a):
            return value

        def _next(msg):
            nonlocal value
            value = next(values)

        self.cc.add_handler(self.number, _next)
        return var([0]).transform(_get)

    def range(self, start, end=None, default=0) -> TimeVar:
        """Range timevar.

        Useful for use with Knobs/Faders.

        Example:
            >>> d2 >> bass('s...', lpf=cc(18).range(500, 5000))
        """
        value = default

        def _get(a):
            return value

        def _set(msg):
            nonlocal value
            value = self.cc.range(start, end, msg.value)

        self.cc.add_handler(self.number, _set)
        return var([0]).transform(_get)


@dataclass
class CC:
    """
    MIDI Control Change Messages.

    Example:

        # See which MIDI's are available
        >>> CC.list_ports()

        # Create a connection
        >>> cc = CC(0)                                # index
        >>> cc = CC('MIDI Mix:MIDI Mix MIDI 1 28:0')  # literal string

        # Add a function to see which events are received
        >>> cc(lambda msg: print(msg.control_number))

        # or use a decorator
        >>> @cc
        ... def _(msg: cc.Msg):
        ...     print(msg.control_number)

        # Alternate between values, useful for the buttons
        >>> d1 >> play('x.', amp=cc(1).switch(1,0))

        # Use Knobs/Fader to control values with Range

        >>> d2 >> bass('s...', lpf=cc(18).range(500, 5000))

        # Map your own functions
        >>> @cc(1)
        ... def _(msg):
        ...     d1.amp = not d1.amp
        ...     d2.amp = not d2.amp
        ...     if d2.amp:
        ...         d3 >> play('x-')

        # Close the connection
        >>> cc.close()
    """

    @classmethod
    def list_ports(cls):
        """Print the list of available ports."""
        list_input_ports()

    @classmethod
    def range(cls, start, end, value, max_value=127) -> float:
        """Get value in a range."""
        if end is None:
            end = start
            start = 0
        if end <= start:
            raise ValueError('Invalid range')

        return (end - start) * (value / max_value) + start

    port: str
    """MIDI port."""
    debug: bool = False
    """Debug active."""
    note_off: bool = False
    """Tump Note-off, False by default."""

    device: 'rtmidi.MidiIn' = field(init=False)
    """MIDI connection."""
    _handlers: defaultdict[str, list[Callable[['CC.Msg'], None]]] = field(
        init=False,
    )
    """Handlers mapped."""

    @dataclass
    class Msg:
        """Controler message."""

        control_function: int
        control_number: int
        value: int
        deltatime: float

        @property
        def cf(self) -> int:
            """Alias to control_function."""
            return self.control_function

        @property
        def cn(self) -> int:
            """Alias to control_number."""
            return self.control_number

    def __post_init__(self):
        """Connect to midi."""
        try:
            device, port_name = open_midiinput(self.port, interactive=False)
        except (rtmidi.InvalidPortError, rtmidi.NoDevicesError) as exc:
            msg = (
                f'Port {self.port} not found, '
                f'the available are: \n\t{self.list_ports()}'
            )
            raise ValueError(msg) from exc

        print(f'Connection |> {port_name}')
        self.port = port_name
        self.device = device
        self.device.set_callback(self._dispatch)
        self._handlers = defaultdict(list)

    @overload
    def __call__(self) -> Controler: ...

    @overload
    def __call__(self, number: int, /) -> Controler: ...

    @overload
    def __call__(self, func: Handler, /) -> Handler: ...

    @overload
    def __call__(self, number: int, func: Handler, /) -> Handler: ...

    @overload
    def __call__(self, number: Handler, func: Handler, /) -> Handler: ...

    def __call__(self, number=None, func=None, /):
        """Control change."""
        control_number = str(number)
        if number is None or callable(number):
            control_number = 'all'
        if callable(number) and func is None:
            func = number

        if func is None:
            return Controler(self, control_number)
        if callable(func):
            return self.add_handler(control_number, func)

    def close(self):
        """Close the active port."""
        self.device.close_port()

    def add_handler(
        self, control_number: str, func: Handler, *, unique: bool = False
    ) -> Handler:
        """Add a handler."""
        if not unique:
            func.__name__ = 'uq_' + uuid4().hex
            self._handlers[control_number].append(func)
            return func

        exists = [
            handle
            for handle in self._handlers[control_number]
            if handle.__name__ == func.__name__
        ]
        if exists:
            index = self._handlers[control_number].index(exists[0])
            self._handlers[control_number][index] = func
        else:
            self._handlers[control_number].append(func)

        return func

    def _dispatch(self, event: tuple[tuple[int, int, int], float], data=None):
        (control_function, control_number, value), deltatime = event
        msg = self.Msg(control_function, control_number, value, deltatime)

        if msg.control_function == NOTE_OFF and not self.note_off:
            return

        if self.debug:
            print(f'{msg=}  <|>  {data=}')

        for handle in chain(
            self._handlers['all'], self._handlers[str(control_number)]
        ):
            try:
                handle(msg)
            except Exception:
                print(format_exc())


if 'midiconstants' in globals():
    for c in filter(str.isupper, dir(midiconstants)):
        setattr(CC, c, getattr(midiconstants, c))
