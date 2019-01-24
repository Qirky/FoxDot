# Background
I wanted to add a voice to my Live Coding compositions so I made some research and I learned about singing synthesis, something not so popular in the occidental world but quite popular in japan, with some really successful brands such as Vocaloid.

Looking for open source singing synthezisers, I found sinsy.jp, It is a website made by people from Nagoya Institute of Technology to convert music sheets (In musicXML format) into a singing voice. This is an open source project, I tried to use it locally but it doesn't have as good quality as the web version, probably it needs some configuration or training that I am not aware of.

# Description
The feature basically converts the notes and durations into a MIDI file, then converts it to a musicXML with musescore and the lyrics are added with a python script. Finally it makes a request to sinsy.jp to create the WAV file.

# Dependencies
There are some dependencies in the code, such as python libraries, shell commands and external software I used to make it work, they could probably be modified to make it more portable.

### Libraries

- MIDIUtil (```pip install MIDIUtil```)

### Shell commands and external software:

- musescore (To convert midi to musicXML which is the format expected by sinsy.jp)
- shell commands (curl, cp, grep)

# Usage

The feature provides the method vrender which has the following parameters
- name: the name of the wav file which is then reproduced with a loop or play method
- dur: specifies duration of each note
- notes: specifies the notes
- lyrics: Is a string which is splitted by spaces
- tempo: singinig velocity in BPM (optional)
- scale: By default major (optional)

A demonstration video can be found [here](https://youtu.be/cgZuO78tVVE) (The command usage in the video is outdated, the interface is a little bit more simple now).

### Command description, with default values
```
vrender(NOTES, file="v1", lyrics="o", dur=[1],sex="female")

```

There might be more notes than words or specified durations, in that case those are extended repeating the string or list respectively.


### Example using all parameters
```
from .Extensions.VRender import vrender

vrender([0,2,0,4], file="wavName", lyrics="hey ho lets go", dur=[1,1,1,1],sex="male")

v1 >> loop('wavName',P[4:12],dur=1)

```


### Example using only the notes
```
from .Extensions.VRender import vrender

vrender([3,2,1,0,4,4,4,4])

v1 >> loop('v1',P[4:12],dur=1)

```
