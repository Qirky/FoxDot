""" Module for converting streams and frequencies """
from __future__ import absolute_import, division, print_function

try:
    import rtmidi
    from rtmidi import midiconstants
    TIMING_CLOCK          = midiconstants.TIMING_CLOCK
    SONG_POSITION_POINTER = midiconstants.SONG_POSITION_POINTER
    SONG_START            = midiconstants.SONG_START
except ImportError as _err:
    pass

from .Patterns import asStream
from .Scale    import ScalePattern
from .TimeVar  import TimeVar

def miditofreq(midinote):
    """ Converts a midi number to frequency """
    return 440 * (2 ** ((midinote - 69.0)/12.0))

midi2cps = miditofreq # alias

def midi(scale, octave, degree, root=0, stepsPerOctave=12):
    """ Calculates a midinote from a scale, octave, degree, and root """

    # Make sure we force timevars into real values

    if isinstance(scale, ScalePattern):

        if isinstance(scale.data, TimeVar):

            scale = asStream(scale.data.now())

    # Force float
    octave = float(octave)   
    degree = float(degree)
    root   = float(root)
    
    # Floor val
    lo = int(degree)
    hi = lo + 1

    octave = octave + (lo // len(scale))

    chroma = range(int(stepsPerOctave))

    scale_val = (scale[hi % len(scale)] - scale[lo % len(scale)]) * ((degree-lo)) + scale[lo % len(scale)]

    midival = scale_val + (octave * len(chroma)) + float(root)

    return midival


class MidiIn:
    metro = None
    def __init__(self, port_id=0):
        """ Class for listening for MIDI clock messages
            from a midi device """
        try:

            self.device = rtmidi.MidiIn()

        except NameError:

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

    def update(self):
        data = self.device.get_message()
        if data is not None:
            datatype, delta = data
            if TIMING_CLOCK in datatype:
                self.pulse += 1
                self.delta += delta
                if self.pulse == self.ppqn:
                    self.bpm = 60.0 / self.delta
                    self.pulse = 0
                    self.delta = 0.0
            elif SONG_POSITION_POINTER in datatype:
                self.metro.set_time(datatype[1] / 4)
        return

    def get_beat(self):
        """ If a beat value has been set, return it, otherwise return None """
        val, self.beat = self.beat, None
        return val

    def close(self):
        """ Closes the active port """
        self.device.close_port()
        return
                
from .SCLang import SynthDefProxy

class MidiOut(SynthDefProxy):
    def __init__(self, degree=0, **kwargs):
        SynthDefProxy.__init__(self, self.__class__.__name__, degree, kwargs)

class MIDIDeviceNotFound(Exception):
    def __str__(self):
        return self.__class__.__name__ + " Error"

class rtMidiNotFound(Exception):
    def __str__(self):
        return self.__class__.__name__ + ": Module 'rtmidi' not found"


if __name__ == "__main__":

    a = MidiIn()

    


        
