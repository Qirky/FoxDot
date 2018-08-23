# Background
I wanted to add a voice to my LiveCoding compositions so I made some research and I learned about singing synthesis, something not so popular in the occidental world but quite popular in japan, with some really successful brands such as Vocaloid.

Looking for open source singing synthezisers, I found sinsy.jp, It is a website made by people from Nagoya Institute of Technology to convert music sheets (In musicXML format) into a singing voice. This is an open source project, I tried to use it locally but it doesn't have as good quality as the web version, probably it needs some configuration or training that I am not aware of.

# Description
The feature basically converts the notes and durations into a MIDI file, then converts it to a musicXML with musescore and the lyrics are added with a python script. Finally it makes a request to sinsy.jp to create the WAV file.

# Dependencies
There are some dependencies in the code, such as python libraries, shell commands and external software I used to make it work, they could probably be modified to make it more portable.

### Libraries

- MIDIUtil
- urllib

### Shell commands and external software:

- musescore (To convert midi to musicXML which is the format expected by sinsy.jp)
- shell commands (curl, cp, grep)

# Usage

The feature provides the method vrender which has the following parametrs
- name: the name of the wav file which is then reproduced with a loop or play method
- dur: specifies duration of each note
- notes: specifies the notes
- lyrics: Is a string which is splitted by spaces
- tempo: singinig velocity in BPM(optional)
- scale: By default major (optional)

### Example
```
vrender("wavName", lyrics="hey ho lets go", notes=[0,2,0,4], dur=[1,1,1,1],tempo=120,scale=Scale.minor)
```
