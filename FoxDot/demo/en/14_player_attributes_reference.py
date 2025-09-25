# Tutorial 14: Player Attributes Reference
# --- TODO: this needs updating


# To see all attributes:
print(Player.get_attributes())

# You can see what effects are available by evaluating
print(FxList)

# Let's use the high pass filter for an example. You can see it's described
# like so:
# "<Fx 'highPassFilter' -- args: hpr, hpf>"

# Each effect has a "master" argument and then child arguments. Here the
# master argument is "hpf" (short for high pass filter) and the child argument
# is "hpr" (short for high pass resonance). The effect is only added when the
# master argument is non-zero:
d1 >> dirt([0,4,2,1], dur=1/2, hpf=4000)

# This sets the high pass filter to 4000 Hz so only frequences in the audio
# signal *above* that are actually heard. Let's change the resonance value. It's
# default value is 1, so let's make it smaller
d1 >> dirt([0,4,2,1], dur=1/2, hpf=4000, hpr=0.3)


# Notice a difference? We can use patterns / vars in our effects to make them
# change over time:
d1 >> dirt([0,4,2,1], dur=1/2, hpf=linvar([0,4000],8), hpr=P[1,1,0.3].stretch(8))




####################
# Reference
####################



####################
# amp - Amplitude (defaults to 1)
# Sets the volume of the note/pattern

d1 >> play("*", dur=1/2, amp=1)

# Half Volume
d1 >> play("*", dur=1/2, amp=.5)

# Creating a pattern with amp
d1 >> play("*", dur=1/2, amp=[1,0,1,1,0])



####################
# amplify - Changes amp, by multiplying agasint the existing value (instead of overwritting)

# Creating a pattern with amp
d1 >> play("*", dur=1/2, amp=[1,0,1,1,0])
d1 >> play("*", dur=1/2, amplify=[.5,1,0])

# Set up a "drop" in the music (Plays at full volume for 28, then 0 for 4)
p1 >> blip([0,1,2,3], amplify=var([1,0],[28,4]))



####################
# bend



####################
# benddelay - See bend



####################
# bits
# The bit depth, in number of bits, that the signal is reduced to;
# this is a value between 1 and 24 where other values are ignored.
# Use crush to set the amount of reduction to the bitrate (defaults to 8)



####################
# bitcrush - See bits



####################
# blur



####################
# bpf - Band Pass Filter



####################
# bpnoise - See bpf



####################
# bpr - See bpf



####################
# bpm



####################
# buf



####################
# channel



####################
# chop
# 'Chops' the signal into chunks using a low frequency pulse wave over the sustain of a note.



####################
# coarse



####################
# comb delay - See echo



####################
# crush



####################
# cut
# Cuts a duration
p1 >> pluck(P[:8], dur=1/2, cut=1/8)
p1 >> pluck(P[:8], dur=1/2, cut=1/4)
p1 >> pluck(P[:8], dur=1/2, cut=1/2)



####################
# cutoff



####################
# decay - See echo



####################
# degree - The degree of the note, or pitch, can be specified by keyword (also the first positional)
p1 >> blip(degree=[0,1,2,3])

# Which is the same as:
p1 >> blip([0,1,2,3])

# Only plays the "root" note of the chord
b1 >> bass(p1.degree[0])



####################
# delay - A duration of time to wait before sending the information to SuperCollider (defaults to 0)

# Delays every 3 note by .1
p1 >> blip([0,1,2,3], delay=[0,0,0.1])

# Delays every 3 note by .5
p1 >> blip([0,1,2,3], delay=[0,0,0.5])

# Plays the note once for each different delays
p1 >> blip([0,1,2,3], delay=(0,0.1))

p1 >> blip([0,1,2,3], delay=(0,0.25))

p1 >> blip([0,1,2,3], delay=(0,.1,.2,.3))



####################
# dist



####################
# dur - Durations (defaults to 1 and 1/2 for the Sample Player)



####################
# echo
# Title keyword: echo, Attribute keyword(s): decay
# Sets the decay time for any echo effect in beats, works best on Sample Player (defaults to 0)
# Multiplied against the sustain value
d1 >> play("x-o-", echo=0.1)

d1 >> play("x-o-", echo=0.5)

p1 >> pluck(P[:8], echo=.25)

p1 >> pluck(P[:8], echo=.5)

p1 >> pluck(P[:8], echo=.5, decay=.5)



####################
# env



####################
# fmod



####################
# formant



####################
# freq



####################
# hpf - High Pass Filter
# Filters out all the frequencies below given value, removing lower freqencies

# 4000 hertz
p1 >> pluck(P[:8], dur=1/2, hpf=4000)

# HPF is 0 for 4 beats, then 4000 for 4 beats
p1 >> pluck(P[:8], dur=1/2, hpf=var([0,4000],[4,4]))

# Linear change on hpf from 0 take 4 beats to get to 4000, 4 beats back to 0
p1 >> pluck(P[:8], dur=1/2, hpf=linvar([0,4000],[4,4]))

# Linear change on hpf from 0 take 8 beats to get to 4000, then reset back to 0
p1 >> pluck(P[:8], dur=1/2, hpf=linvar([0,4000],[8,0]))

# With resonance change (default is 1)
p1 >> pluck(P[:8], dur=1/2, hpf=linvar([0,4000],[8,0]), hpr=.5)

# With resonance change as a linvar
p1 >> pluck(P[:8], dur=1/2, hpf=linvar([0,4000],[8,0]), hpr=linvar([0.1,1],12))



####################
# hpr - See hpf



####################
# lpf - Low Pass Filter
# Filters out all the frequencies above given value, removing higher freqencies

# 4000 hertz
p1 >> pluck(P[:8], dur=1/2, lpf=400)

# With resonance change as a linvar
p1 >> pluck(P[:8], dur=1/2, lpf=linvar([500,4000],[8,0]), lpr=linvar([0.1,1],12))



####################
# lpr - See lpf



####################
# midinote



####################
# pan
# Panning, where -1 is far left, 1 is far right (defaults to 0)



####################
# pitch - See degree



####################
# pshift



####################
# oct



####################
# rate
# Variable keyword used for misc. changes to a signal. E.g. Playback rate of the Sample Player (defaults to 1)



####################
# room
# Title keyword: room, Attribute keyword(s): mix

# The room argument specifies the size of the room
d1 >> play("x-o-", room=0.5)

# Mix is the dry/wet mix of reverb or how much the reverb is mixed with the source.  1 is all reverb, 0 is no reverb at all. (Default 0.1)
d1 >> play("x-o-", room=0.5, mix=.5)



####################
# Reveb
# See Room



####################
# sample
# Special keyword for Sample Players; selects another audio file from the bank of samples for a sample character.



####################
# scale



####################
# shape



####################
# slide - Slide To
# Slides' the frequency value of a signal to freq * (slide+1) over the duration of a note (defaults to 0)

p1 >> pluck(P[:8], dur=1/2, slide=1)

p1 >> pluck(P[:8], dur=1/2, slide=12)

p1 >> pluck(P[:8], dur=1/2, slide=var([0,-1],[12,4]))



####################
# slidedelay



####################
# slidefrom



####################
# slider



####################
# spread



####################
# spin



####################
# striate



####################
# stutter



####################
# sus - Sustain (defaults to `dur`)



####################
# swell



####################
# vib - Vibrato
# Vibrato - Title keyword: vib, Attribute keyword(s): Vibrato (defaults to 0)

p1 >> pluck(P[:8], dur=1/2, vib=12)

# With child attribute, vibdepth (default 0.2)
p1 >> pluck(P[:8], dur=1/2, vib=12, vibdepth=0.5)



####################
# vibdepth - See vib
