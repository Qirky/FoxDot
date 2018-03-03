# Introduction

FoxDot can also be used to sequence and manipulate audio samples as well as generating sound based on musical instruction. To do this all you need to do is use the special `play` SynthDef. The first argument of the `play` SynthDef should be a string of characters instead of a list of numbers as you would do for any other SynthDef. Each character represents a different audio file, which is stored in a buffer in SuperCollider. To view which character relates to which audio file, execute `print BufferManager`.

## Playing audio files

For our examples we will be using just three samples; 'x' (a bass drum), 'o' (a snare hit), and '-' (a hi-hat). To play these audio files, just use the `play` SynthDef and provide a string of these characters like so:

	p2 >> play("x-o-")

If multiple files exist in a sample directory, the first sample (in alphabetical order) will be played.  In order to play the other samples in the directory, you can target them using the 'sample' parameter, like this:

	p2 >> play("a", sample=2)
	
This will play the third sample in the directory (counting from 0).  You can also play a sequence of samples from a directory by supplying a list to the 'sample' parameter:
	
	p2 >> play("a", sample=[0,1,2,3])
	
This will play the first, second, third, and fourth samples in order.  In this example, if there were no fourth sample, playback would 'wrap around' and use the first sample in the list instead.

## Manipulating the sequence

## Using your own audio files

You can use your own samples by simply dropping audio files into the existing FoxDot sample directories; these are found in the 'snd' directory in the root of the FoxDot installation (e.g., 'C:\Python27\Lib\site-packages\FoxDot\snd').

