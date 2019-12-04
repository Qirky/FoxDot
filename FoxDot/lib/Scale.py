from __future__ import absolute_import, division, print_function

from .Patterns import Pattern, PGroup, asStream
from .TimeVar import TimeVar
from .Root import Root

from random import choice
from copy import copy
import math

def miditofreq(midinote):
    """ Converts a midi number to frequency """
    return 440 * (2 ** ((midinote - 69.0)/12.0))

def _log2(num):
    return math.log(num) / math.log(2)

def freqtomidi(freq):
    return 12 * _log2((freq / 440)) + 69

def midi(scale, octave, degree, root=0, stepsPerOctave=12):
    """ Calculates a midinote from a scale, octave, degree, and root """

    # Make sure we force timevars into real values

    if isinstance(scale, ScalePattern) and isinstance(scale.data, TimeVar):

        scale = asStream(scale.data.now())

    # Force float
    octave = float(octave)
    degree = float(degree)
    root   = float(root)
    
    # Floor val
    lo = int(math.floor(degree))
    hi = lo + 1

    octave = octave + (lo // len(scale))
    index  = lo % len(scale)

    # Work out any microtones

    micro = (degree - lo)

    if micro > 0:

        ex_scale = list(scale) + [stepsPerOctave]

        diff  = ex_scale[index + 1] - scale[index]

        micro = micro * diff

    midival = stepsPerOctave * octave # Root note of scale
    midival = midival + root          # Adjust for key
    midival = midival + scale[index]  # Add the note
    midival = midival + micro         # And any microtonal

    return midival

def get_freq_and_midi(degree, octave, root, scale):
    """ Returns the frequency and midinote """

    # TODO -- make sure it's always a scale
    if hasattr(scale, "now"):

        scale = scale.now()

    if isinstance(scale, ScaleType):

        freq, midinote = scale.get_freq(degree, octave, root, get_midi=True)

    else:

        midinote = midi(scale, octave, degree, root)
        freq     = miditofreq(midinote)

    return freq, midinote

class ScaleType:
    pass

class TuningType(list):
    def __init__(self, data):
        data = list(data)
        list.__init__(self, data[:-1])
        self.steps = int(data[-1])

class Tuning:
    ET12          = TuningType([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    just          = TuningType([0.0, 1.1173128526978, 2.0391000173077, 3.1564128700055, 3.8631371386483, 4.9804499913461, 5.9022371559561, 7.0195500086539, 8.1368628613517, 8.8435871299945, 10.175962878659, 10.882687147302, 12 ])
    bohlen_pierce = TuningType([i*12/13*math.log(3, 2) for i in range(14)])

class ScalePattern(ScaleType, Pattern):

    name = None

    def __init__(self, semitones, name=None, tuning=Tuning.ET12):

        self.name = name

        self.semitones = semitones.data if isinstance(semitones, Pattern) else semitones

        if not isinstance(tuning, TuningType):

            self.tuning = TuningType(tuning)

        else:

            self.tuning = tuning

        self.data = self.semitones

        self.steps = self.tuning.steps

        if self.steps:

            self.pentatonic = PentatonicScalePattern(self)

    def __eq__(self, other):
        return self.name == other.name if isinstance(other, ScalePattern) else False

    def __ne__(self, other):
        return self.name != other.name if isinstance(other, ScalePattern) else True

    def semitones(self, pitches):
        """ Returns the semitone values for a series of pitches in this scale """
        tones = []
        for pitch in asStream(pitches):
            tones.append( self.note_to_semitone(pitch) )
        return Pattern(tones)

    def get_tuned_note(self, degree):
        tuning_index = int(self[degree]) % len(self.tuning)
        # tuning_offset = 0
        # if degree < 0:
        #     tuning_offset = (((abs(degree) // len(self.tuning)) + 1) * self.steps)
        return self.tuning[tuning_index]

    def get_midi_note(self, degree, octave=5, root=0):
        """ Calculates a midinote from a scale, octave, degree, and root """

        # Make sure we force timevars into real values

        if isinstance(self.data, TimeVar):

            scale = asStream(self.data.now())

        # Force float
        octave = float(octave)
        degree = float(degree)
        root   = float(root)
        
        # Floor val
        lo = int(math.floor(degree))
        hi = lo + 1

        octave = octave + (lo // len(self))
        index  = lo % len(self)

        pitch = self.get_tuned_note(index)

        # Work out any microtones

        micro = (degree - lo)

        if micro > 0:

            ex_scale = list(self) + [self.steps]

            diff  = ex_scale[index + 1] - self[index]

            micro = micro * diff

        midival = self.steps * octave    # Root note of scale
        midival = midival + root         # Adjust for key
        midival = midival + pitch        # Add the note
        midival = midival + micro        # And any microtones
        
        return midival

    def get_freq(self, degree, octave=5, root=0, get_midi=False):
        """ Returns the frequency of a midinote calculated by self.get_midi_note. Returns a tuple containing
            the freqency and midinote if `get_midi` is set to `True`. """
        midinote = self.get_midi_note(degree, octave, root)
        return (miditofreq(midinote), midinote) if get_midi else miditofreq(midinote)

    def note_to_semitone(self, pitch):
        """ Takes a pitch value and returns the semitone value e.g. midinote value not accounting for octaves """
        if isinstance(pitch, PGroup):
            return pitch.__class__([self.note_to_semitone(p) for p in pitch])
        else:
            i = pitch % len(self.data)
            n = (pitch // len(self.data)) * self.steps 
        return asStream(self.data)[i] + n

    def getslice(self, start, stop, step=1):
        """ Called when using __getitem__ with slice notation. Numbers 
            smaller than 0 and greater than the max value are adjusted. """
        
        start = start if start is not None else 0
        stop  = stop if stop is not None else len(self)
        step  = step if step is not None else 1

        if stop < start:

            stop = (len(self.data) +  stop)

        semitones = []

        for i in range(start, stop, step):

            # Get the semitone

            tone = self[i]

            # Negative values

            if i < 0:

                sub = (((abs(i) // len(self)) + 1) * self.steps)

                tone -= sub

            # Values past the end

            elif i >= len(self):

                add = ((i // len(self)) * self.steps)

                tone += add

            semitones.append(tone)

        return ScalePattern(semitones)

    #def semitone_to_note(self, semitone):
    #    """ Takes a semitone value (midinote) and returns the pitch in this scale """
    #    return semitone


class PentatonicScalePattern(ScalePattern):

    def __init__(self, scale):

        self.update(scale)

    def update(self, scale):

        self.data      = scale
        self.steps     = scale.steps
        self.semitones = scale.semitones
        self.tuning    = scale.tuning

    def __len__(self):
        return 5

    @staticmethod
    def values(scale):

        shift = ((scale[2]-scale[0]) % 2) * 2

        return sorted([scale[(i+shift)%len(scale)] for i in range(0,5*4,4)])

    def __str__(self):
        return str(self.values(self.data))

    def __repr__(self):
        return str(self)

    def __iter__(self):

        for note in self.values(self.data):

            yield note

    def __getitem__(self, key):
        return self.values(self.data)[int(key)]

class FreqScalePattern(ScalePattern):
    def __init__(self):
        ScalePattern.__init__(self, [], name="freq")
    def get_midi_note(self, freq, *args, **kwargs):
        return freqtomidi(freq)
    def get_freq(self, freq, *args, **kwargs):
        return (freq, freqtomidi(freq)) if kwargs.get("get_midi", False) else freq
    def __repr__(self):
        return "[inf]"

class _DefaultTuning(TuningType):
    """ Wrapper for Tuning.default """
    def __init__(self, tuning):
        self.tuning = tuning

    def __len__(self):
        return len(self.tuning)

class _DefaultScale(ScaleType):
    """ Wrapper for Scale.default """
    def __init__(self, scale):
        self.scale = copy(scale)
        self.pentatonic = copy(self.scale.pentatonic)

    def __len__(self):
        return len(self.scale)

    def __repr__(self):
        return repr(self.scale)

    def __iter__(self):
        return self.scale.__iter__()

    def set(self, new, *args, **kwargs):
        """ Change the contents of the default scale """

        if type(new) == str:

            self.scale = Scale.get_scale(new)

            if "tuning" in kwargs:

                self.scale.tuning = kwargs["tuning"]

            self.pentatonic.update(self.scale.pentatonic)

        elif isinstance(new, (list, Pattern, TimeVar)):

            self.scale = ScalePattern(new, *args, **kwargs)

            # Store if the user has used a name

            if self.scale.name is not None and self.scale.name not in Scale.names():

                Scale[self.scale.name] = self.scale

            self.pentatonic.update(self.scale.pentatonic)

        else:

            print("Warning: {!r} is not a valid scale".format(new))

        return self

    def __getattribute__(self, attr):
        if attr not in ("scale", "set", "pentatonic"):
            return self.scale.__getattribute__(attr)
        else:
            return object.__getattribute__(self, attr)

    # Python2
    def __getattr__(self, attr):
        return self.__getattribute__(attr)

# Custom made fibonacci tuing

##fib = [0,1]
##for n in range(2,11):
##    fib.append(fib[n-1]+fib[n-2])
##
##fibonacci = []
##for n in range(3, len(fib)-1):
##    fibonacci.append((n-3) * (fib[n] / float(fib[n-1])))
##
##fibonacci = Scale("fibonacci", fibonacci)
##
##del n

class __scale__:

    chromatic       = ScalePattern([0,1,2,3,4,5,6,7,8,9,10,11], name="chromatic")

    major           = ScalePattern([0,2,4,5,7,9,11], name="major")
    majorPentatonic = ScalePattern([0,2,4,7,9], name="majorPentatonic" )

    minor           = ScalePattern([0,2,3,5,7,8,10], name="minor")
    aeolian         = ScalePattern([0,2,3,5,7,8,10], name="aeolian")
    minorPentatonic = ScalePattern([0,3,5,7,10], name="minorPentatonic")

    mixolydian      = ScalePattern([0,2,4,5,7,9,10], name="mixolydian")

    melodicMinor    = ScalePattern([0,2,3,5,7,9,11], name="melodicMinor")
    melodicMajor    = ScalePattern([0,2,4,5,7,8,11], name="melodicMajor")

    harmonicMinor   = ScalePattern([0,2,3,5,7,8,11], name="harmonicMinor")
    harmonicMajor   = ScalePattern([0,2,4,5,7,8,11], name="harmonicMajor")

    # Goal: Do normal scales but adjust tuning

    justMajor       = ScalePattern([0,2,4,5,7,9,11], name="justMajor", tuning=Tuning.just)
    justMinor       = ScalePattern([0,2,3,5,7,8,10], name="justMinor", tuning=Tuning.just)

    dorian          = ScalePattern([0,2,3,5,7,9,10], name="dorian")
    dorian2         = ScalePattern([0,1,3,5,6,8,9,11], name="dorian2") 
    diminished      = ScalePattern([0,1,3,4,6,7,9,10], name="diminished")

    egyptian        = ScalePattern([0,2,5,7,10], name="egyptian")
    yu              = ScalePattern([0,3,5,7,10], name="yu")
    zhi             = ScalePattern([0,2,5,7,9], name="zhi")
    phrygian        = ScalePattern([0,1,3,5,7,8,10], name="phrygian")
    prometheus      = ScalePattern([0,2,4,6,11], name="prometheus")
    indian          = ScalePattern([0,4,5,7,10], name="indian")

    locrian         = ScalePattern([0,1,3,5,6,8,10], name="locrian")
    locrianMajor    = ScalePattern([0,2,4,5,6,8,10], name="locrianMajor")

    lydian          = ScalePattern([0,2,4,6,7,9,11], name="lydian")
    lydianMinor     = ScalePattern([0,2,4,6,7,8,10], name="lydianMinor")

    custom          = ScalePattern([0,2,3,5,6,9,10], name="custom")

    hungarianMinor  = ScalePattern([ 0, 2, 3, 6, 7, 8, 11 ], name="hungarianMinor")
    romanianMinor   = ScalePattern([ 0, 2, 3, 6, 7, 9, 10 ], name="romanianMinor")
    chinese         = ScalePattern([ 0, 4, 6, 7, 11 ], name="chinese")

    wholeTone       = ScalePattern([ 0, 2, 4, 6, 8, 10 ], name="wholeTone")

    # Half-Whole Diminished Scale - halfWhole
    halfWhole       = ScalePattern([ 0, 1, 3, 4, 6, 7, 9, 10 ], name= "halfWhole")
    # Whole-Half Diminished Scale - wholeHalf
    wholeHalf       = ScalePattern([ 0, 2, 3, 5, 6, 8, 9, 11 ], name= "wholeHalf")
    
    ### Bebop Scales ###
    bebopMaj        = ScalePattern([ 0, 2, 4, 5, 7, 8, 9, 11 ], name="bebopMaj")
    bebopDorian     = ScalePattern([ 0, 2, 3, 4, 5, 9, 10 ], name="bebopMin") # aka Bebop Minor
    bebopDom        = ScalePattern([ 0, 2, 4, 5, 7, 9, 10, 11 ], name="bebopDom") # Bebop Dominant/Mixolydian
    bebopMelMin     = ScalePattern([ 0, 2, 3, 5, 7, 8, 9, 11 ], name="bebopMelMin") # Bebop Melodic Minor
    blues           = ScalePattern([ 0, 3, 5, 6, 7, 10 ], name="blues")

    ### Modes of the Melodic Minor Scale ###
    
    # First mode - Min/Maj chord
    minMaj         = ScalePattern([ 0, 2, 3, 5, 7, 9, 11 ], name= "minMaj")
    # Second mode - (x)susb9
    susb9          = ScalePattern([ 0, 1, 3, 5, 7, 9, 10 ], name= "susb9")
    # Third Mode - Lydian Augmented, (x)Maj7#5
    lydianAug      = ScalePattern([ 0, 2, 4, 6, 8, 9, 11 ], name= "lydianAug")
    # Fourth Mode - Lydian Dominant, (x)7#11
    lydianDom      = ScalePattern([ 0, 2, 4, 6, 7, 9, 10 ], name= "lydianDom")
    # Fifth Mode - seldom used, but it's IMinMaj/V
    melMin5th      = ScalePattern([ 0, 2, 4, 5, 7, 8, 10 ], name= "melMin5th")
    # Sixth Mode - half-diminished (aka Locrian #2), (x)half-diminished
    halfDim      = ScalePattern([ 0, 2, 3, 5, 6, 8, 10 ], name= "halfDim")
    # Seventh Mode - altered (diminished whole-tone), (x)7alt
    altered      = ScalePattern([ 0, 1, 3, 4, 6, 8, 10 ], name= "altered")
    


    freq            = FreqScalePattern()

    def __init__(self):

        self.default = _DefaultScale(self.major)

    def __setattr__(self, key, value):
        if key == "default" and key in vars(self):
            self.default.set(value)
        else:
            self.__dict__[key] = value
        return

    def __getitem__(self, key):
        return getattr(self, key)

    def get_scale(self, name):
        """ Returns a ScalePattern using a name """
        return self.library()[name]

    def library(self):
        """ Returns a dictionary with scale names to scale instances """
        lib = []
        for items in (self.__class__.__dict__.items(), self.__dict__.items()):
            lib.extend([(key, value) for key, value in items if isinstance(value, ScalePattern)])
        return dict(lib)

    def names(self):
        """ Returns a list of all the scale names """
        return sorted(self.library().keys())

    def scales(self):
        """ Returns a list of all the scales object """
        return sorted(self.library().values(), key=lambda scale: scale.name)

    def choose(self):
        """ Scale.choose() -> Returns a random scale object """
        return choice(self.scales())


Scale = __scale__()


# class Chord:
#     def __init__(self):
#         self.scale = Scale.default
#         self.root  = Root.default
