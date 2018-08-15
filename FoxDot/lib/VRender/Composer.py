from MidiFactory import createMidi
import os

def extendScale(scale,times):
    scaleAux = scale[:]
    for i in range(1,times):
        for note in scaleAux:
            scale.append(note+12*i)
    return scale

def toList(rhythm, melody, scale):

    scale = extendScale(scale,2)
    scaleSize = len(scale)

    volume = 100
    baseNote = 60

    composition = []
    time = 0
    for i in range(len(rhythm)):
        dur = rhythm[i]
        note = scale[melody[i]%scaleSize] + baseNote
        composition.append((note,dur,volume,time))
        time += dur

    return composition

def compose(notes,durations,scale, new_midi_path, new_musicxml_path):

    print(notes)
    print(durations)
    print(scale)

    composition = toList(durations,notes,scale)
    print(composition)
    createMidi(new_midi_path, composition)
    os.system("musescore "+ new_midi_path +" -o " + new_musicxml_path)