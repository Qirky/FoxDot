from midiPlayer import createMidi

def silenceToTempo(char):
    #Notation for silences
    # S == 4 BPM
    # s == 2 BPM
    # any other alphabetic character == 1 BMP
    if char == "S":
        return 4
    elif char == "s":
        return 2
    else:
        return 1
        
def toList(rhythms, melodies, repetitions, total,scale):

    assert(len(scale) == 7)
    scaleAux = scale[:]
    for note in scaleAux:
        scale.append(note+12)
    assert(len(scale) == 14)

    lista = []
    for k in range(repetitions):
        for j in range(len(rhythms)):
            rhythm = rhythms[j]
            melody = melodies[j]
            time = 0 + total*k
            for i in range(len(rhythm)):
                char = rhythm[i]
                if char.isdigit():
                    dur = int(char)
                    note = scale[int(melody[i])%14] + 60
                    lista.append([(note,dur,100, time)])
                    time += dur
                else:
                    time += silenceToTempo(char)
    return lista

def parse(stringList):
    return stringList.split()

def main(argv):
    print(argv)
    notes = parse(argv[0])
    durations = parse(argv[1])
    scale = list(map(int,parse(argv[2])))

    print(notes)
    print(durations)
    print(scale)

    composition = toList([durations],[notes],1,sum(list(map(int,durations))),scale)
    print(composition)
    createMidi(LAST_MIDI, composition)

import sys
if __name__ == "__main__":
    main(sys.argv[1:])