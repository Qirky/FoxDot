from FoxDot.lib.Players import rest

def melody(s,n_bars=1,base_duration=4,verbose=False):
    """
    Convert a melody string to triple of note values,
    note durations and note sustain values.

    A melody string could look something like this:

    >>> s = "0123"

    which translates to ``Cut the bar in four fourth notes,
    whith values [ 0, 1, 2, 3].''

    Another example would be

    >>> s = "0.1.2.3."

    which translates to ``Cut the bar in eight eigths,
    but play only four eights notes, each of which is followed
    by an eigth rest. Note values like above.``

    Notes can, however, be sustained like so:

    >>> s = "0=1.2.3."

    which is similar to the last case, besides the fact that
    the first note will not be followed by a rest but be 
    sustained until the second note is played. The following 
    string would yield the same melody

    >>> s = "0===1=..2=..3=.."

    Note that in this example, one character corresponds to 
    a 16th note.

    This can become quite messy to overlook, so one may add
    the "|" character as a visual aid. The function will
    ignore this character. The string

    >>> s = "0===|1=..|2=..|3=.."

    would therefore yield the same result as the last two
    strings.

    Final example: melody strings can begin with a rest:

    >>> s = ".0=.|1...|2...|3..."
        

    Parameters
    ==========
    s : str
        The melody string.
    n_bars : int, default = 1
        The number of bars this melody string is supposed to span.
    base_duration : float, default = 4
        The duration of a single bar (in beats).
    verbose : bool, default = False
        Be chatty.

    Returns
    =======
    notes : list of int
        The notes to play.
    durs : list of float
        The corresponding note durations.
    suss : list of float
        The corresponding note sustain values.
    """

    # check if the input is a string
    if type(s) != str:
        raise TypeError("s has to be a String")

    # remove all "|" character as those are supposed to be helpers
    s = s.replace("|","")

    # raise an error if the melody string is empty
    if len(s) == 0:
        raise ValueError("There's no notes in this bar (length 0)")

    # calculate the duration of this whole melody,
    # the total number of notes
    # and duration of a single character
    barlength = base_duration * n_bars
    n_notes = len(s)
    note_duration = barlength / n_notes

    # define empty notes (rests)
    empty = [" ","."]

    # initialize return lists
    notes = []
    durs = []
    suss = []

    # check first character (check whether to begin with a rest)
    i = 0
    initial_note_is_rest = s[0] in empty

    if initial_note_is_rest:

        # this first note is going to be muted, so we just assign value 0
        notes.append(0)

        # while the string contains rests, increase the rest duration
        initial_rest = 0
        while (i<len(s)) and (s[i] in empty):
            initial_rest += note_duration
            i += 1

        durs.append(rest(initial_rest))
        suss.append(rest(initial_rest))

    # process the rest of the fucking string
    while i<len(s):

        # the sustain character may only follow a note or another sustain character
        if s[i] == "=":
            raise ValueError("Can't sustain a rest:\n"+"   "+s+"\n   "+" "*i+"^")

        # assign the current note and the base note duration
        note = int(s[i])
        dur = note_duration
        sus = note_duration

        if verbose:
            print("note:",s[i])

        # proceed to next character
        i += 1

        # for sustain characters following a note, add durations and sustains
        while i<len(s) and (s[i] == "="):
            dur += note_duration
            sus += note_duration
            if verbose:
                print("note:",s[i])
            i += 1

        # for empty/rest characters, only increase the duration and not the sustain
        while i<len(s) and (s[i] in empty):
            dur += note_duration

            if verbose:
                print("note:",s[i])
            i += 1

        # save this note
        notes.append(note)
        durs.append(dur)
        suss.append(sus)

    return notes, durs, suss


def print_melody_string(s):

    notes, dur, sus = melody(s)

    print("====")
    print(s)
    print(notes)
    print(dur)
    print(sus)
    print("====")

if __name__ == "__main__":

    # valid strings 
    print_melody_string("..0.|0104|..2.|.2..")
    print_melody_string("012.")
    print_melody_string("012=")

    # invalid string
    print_melody_string("012..=.")

