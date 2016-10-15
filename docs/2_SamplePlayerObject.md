# Introduction

FoxDot can also be used to sequence and manipulate audio samples as well as generating sound based on musical instruction. To do this all you need to do is use the special `play` SynthDef. The first argument of the `play` SynthDef should be a string of characters instead of a list of numbers as you would do for any other SynthDef. Each character represents a different audio file, which is stored in a buffer in SuperCollider. To view which character relates to which audio file, execute `print BufferManager`.

## Playing audio files

For our examples we will be using just three samples; 'x' (a bass drum), 'o' (a snare hit), and '-' (a hi-hat). To play these audio files, just use the `play` SynthDef and provide a string of these characters like so:

	p2 >> play("x-o-")


## Manipulating the sequence

## Using your own audio files