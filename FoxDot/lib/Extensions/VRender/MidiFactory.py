from midiutil import MIDIFile

def createMidi(midi_file, composition):
    print("Composition:")
    print(composition)

    MyMIDI = MIDIFile(1)

    track = 0
    channel = 0
    for note in composition:
        pitch = note[0]
        duration = note[1] # In beats
        volume   = note[2] # 0-127, as per the MIDI standard
        time = note[3]

        MyMIDI.addNote(track, channel, pitch, time, duration, volume)

    with open(midi_file, "wb") as output_file:
        MyMIDI.writeFile(output_file)