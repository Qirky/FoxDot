""" Module for converting handling MIDI in/out and functions relating to MIDI pitch calculation. """

from __future__ import absolute_import, division, print_function

try:
    import rtmidi
    from rtmidi import midiconstants
    TIMING_CLOCK          = midiconstants.TIMING_CLOCK
    SONG_POSITION_POINTER = midiconstants.SONG_POSITION_POINTER
    SONG_START            = midiconstants.SONG_START
    SONG_STOP             = midiconstants.SONG_STOP 
except ImportError as _err:
    pass

from .Patterns import asStream
from .Scale    import ScalePattern
from .TimeVar  import TimeVar
from .SCLang import SynthDefProxy

import time

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


if __name__ == "__main__":

    a = MidiIn()
