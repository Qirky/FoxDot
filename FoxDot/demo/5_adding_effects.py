# Tutorial 5: Adding effects

# You can effects and filters to your player objects just by adding keyword
# arguments like so:

d1 >> dirt([0,4,2,1], dur=1/2)

d1 >> dirt([0,4,2,1], dur=1/2, room=1) # Adds a reverb

d1.stop()

# You can see what effects are available by evaluating

print(FxList)

# Let's use the high pass filter for an example. You can see it's described
# like so:

"<Fx 'highPassFilter' -- args: hpr, hpf>"

# Each effect has a "master" argument and then child arguments. Here the
# master argument is "hpf" (short for high pass filter) and the child argument
# is "hpr" (short for high pass resonance). The effect is only added when the
# master argument is non-zero:

d1 >> dirt([0,4,2,1], dur=1/2, hpf=4000)

d1.stop()

# This sets the high pass filter to 4000 Hz so only frequences in the audio
# signal *above* that are actually heard. Let's change the resonance value. It's
# default value is 1, so let's make it smaller

d1 >> dirt([0,4,2,1], dur=1/2, hpf=4000)

d1 >> dirt([0,4,2,1], dur=1/2, hpf=4000, hpr=0.3)

d1.stop()

# Notice a difference? We can use patterns / vars in our effects to make them
# change over time:

d1 >> dirt([0,4,2,1], dur=1/2, hpf=linvar([0,4000],8), hpr=P[1,1,0.3].stretch(8))

d1.stop()

# Try playing around with other effects and see what crazy sounds you can make!

