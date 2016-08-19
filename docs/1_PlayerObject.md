# Introduction

FoxDot makes music by creating Player Objects that are given a set of instructions to follow. In Python, objects are usually instantiated (created) with a set of arguments and assigning it to a variable, like so:

	>>> class Animal:
	>>>     def __init__(self, animal):
	>>>        self.type = animal
	>>>
	>>> monty = Animal('dog')
	>>> print monty.type
	dog

If you want to learn more about how to program in Python there are lots of resources online and a good place to start would be the official Python website. FoxDot is written in Python and inherits all of Python's great features but does things slightly differently, however, when it comes to instantiating a Player Object.

## Creating a Player Object

FoxDot doesn't actually make any sounds itself but uses SuperCollider to synthesise sounds. SuperCollider is a hugely powerful tool when it comes to synthesis and digital signal processing but it's accompanied by a steep learning curve. SuperCollider uses something called a SynthDef (essentially a digital instrument) that contains information on how a note should sound when played. Player Objects are pointed to a desired SynthDef and given some instructions on how to use them. To instantiate a Player Object that uses a SynthDef called 'example', you could execute the following code:

	p1 = PlayerObject('p1')

The only problem is, if you want to change the attributes of `p1` you need to use an update method, which requires extra typing, because re-executing the code above creates a new Player Object called MyPlayer and forgets the reference to the first `p1`! This leaves you with two Player Objects and one of them can't (easily) be accessed. To stop this from happening, FoxDot uses a double-arrow syntax to create Player Objects specifically. Instead of using the SynthDef name as an argument when instantiating the Player class, it is used as if it were the class itself like so:

	p1 >> pads()

If a user re-executes the code, FoxDot will update the variable called MyPlayer instead of creating a new one, which means you can make changes to your music using just one line of code.

## Giving your Player instructions

Creating a Player Object with no arguments will just play a single note on middle C repeatedly until stopped. The first argument should be the degree of the note to be played (default is the lowest note of octave 5 of the major scale) and does not need to be specified by name. Python, like most programming languages, using zero-indexing when accessing values in an array, which means that 0 refers to the first note of the scale. Other useful arguments that can be specified are the octave, duration, sustain, and amplitude:

	p1 >> pads([0,4,2,4], dur=1/2, sus=[2,1/2,1/2,1/2], oct=(5,6), amp=0.4)

Arguments can be floating points, fractions, lists, and even tuples. Lists of values are iterated over as the Player plays notes whereas the values in tuples are used simultaneously i.e. MyPlayer will play notes in the 5th and 6th octave together.

## Algorithmic Manipulation

The code below plays the first four notes of the default scale on repeat:

	p1 >> pads([0,1,2,3])

It's possible to manipulate this by adding an array of numbers to the Player object like so

	p1 >> pads([0,1,2,3]) + [0,0,2]

In psedo-code this could be written as "every 3 notes, play two degrees higher". These values can be laced and grouped together:

	p1 >> pads([0,1,2,3]) + [0,1,[0,(0,2)]]

## Changing Scale

By default, Player Objects use the C Major scale. These can be changed by using the keyword arguments 'scale' and 'root'. Scales can be defined as an array of semitones, such that the Major scale is [0,2,4,5,7,9,11] or one of the predefined scales from the Scale module, e.g. Scale.minor. Root refers to the tonic of the scale; 0 being C, 1 is C#, 2 is D and so on.

The default scale can be changed such that any Player not using a specific scale will be updated. This is done using the syntax below (each line is technically equivalent):

	Scale.default.set("major")
	Scale.default.set(Scale.major)
	Scale.default.set([0,2,4,5,7,9,11])

This is the same for the root:

	Root.default.set(1)
	Root.default.set("C#")

## Groups

Attributes of players, such as degree or scale, can also be changed by directly assigning values to it such that

	p1 >> pads([0,2,4,2], scale=Scale.majorPentatonic)

is equivalent to

	p1 >> pads()
	p1.degree = [0,2,4,2]
	p1.scale = Scale.majorPentatonic

This is useful if you want to assign the same values to multiple Player Object simultaneously, like so:

	p1 >> pads([0,2,4,2])
	p2 >> pads([2,1,0,4])
	p3 >> pads([2,3])
	p1.dur=p2.dur=p3.dur=[1,1/2,1/4,1/4]
	
	p1.stop()
	p2.stop()
	p3.stop()

To reduce the amount of typing, Player Objects can be grouped together and their attributes modified in a simpler way:

	p1 >> pads([0,2,4,2])
	p2 >> pads([2,1,0,4])
	p3 >> pads([2,3])
	g1 = group(p1, p2, p3)
	g1.dur=[1,1/2,1/4,1/4]
	
	g1.stop()


----------

For more documentation on the Players module, see Players.py.