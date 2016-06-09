""" Module sed for converting streams and frequencies """

def miditofreq(midinote):
    """ Converts a midi number to frequency """
    return 440 * (2 ** ((midinote - 69.0)/12.0))

def midi(scale, octave, degree, root=0, stepsPerOctave=12):
    """ Calculates a midinote from a scale, octave, degree, and root """

    # Force float
    try:
        degree = float(degree)
    except Exception as e:
        print degree, type(degree)
        raise Exception(e)

    # Floor val
    lo = int(degree)
    hi = lo + 1

    octave = octave + (lo / len(scale))

    chroma = range(stepsPerOctave)

    scale_val = (scale[hi % len(scale)] - scale[lo % len(scale)]) * ((degree-lo)) + scale[lo % len(scale)]

    return scale_val + (octave * len(chroma)) + float(root)
