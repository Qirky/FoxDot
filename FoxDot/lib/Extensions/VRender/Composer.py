from __future__ import absolute_import, print_function

from .MidiFactory import createMidi
import os
from math import ceil

def extendScale(scale,times):
    scaleAux = scale[:]
    for i in range(1,times):
        for note in scaleAux:
            scale.append(note+12*i)
    return scale

def matchListsSize(rhythm,melody):
    n_rhythm =len(rhythm)
    n_melody = len(melody)
    if n_rhythm < n_melody:
        rhythm = (rhythm*int(ceil(n_melody/float(n_rhythm))))[:n_melody]
    elif n_rhythm != n_melody:
        melody = (melody*int(ceil(n_rhythm/float(n_melody))))[:n_rhythm]

    return rhythm,melody

def toList(rhythm, melody, scale):

    scale = extendScale(scale,2)
    scaleSize = len(scale)

    volume = 100
    baseNote = 60

    rhythm, melody = matchListsSize(rhythm,melody)

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