# Tutorial 11: Playing Custom Samples

# You can use your own samples by simply dropping audio files into the existing FoxDot sample directories.
# These are found in the 'snd' directory in the root of the FoxDot installation
# (e.g., 'C:\Python27\Lib\site-packages\FoxDot\snd').

# You saw earlier how to work with samples using play(). You can also play samples with loop().
s1 >> loop('foxdot')

# You may notice that this is just playing the first part of the sample over and over again.
# You can tweak the behavior with many of the arguments we've seen thus far for controlling other synths. dur is a good place to start.
s1 >> loop('foxdot', dur=4)

# If you have a folder full of samples that you would like to use in FoxDot, you can call loop() with the full path to the sample.
s1 >> loop('/path/to/samples/quack.wav')

# If you give loop the path to a folder, it will play the first sample it finds. You can change which sample it plays with the sample= arg.

# Play the first sample in my collection
s1 >> loop('/path/to/samples')

# Play the second sample in my collection
s1 >> loop('/path/to/samples', sample=1)

# If you're going to be using a lot of samples from a folder, you can add it to the sample search path. FoxDot will look under all its search paths for a matching sample when you give it a name.
Samples.addPath('/path/to/samples')
s1 >> loop('quack')

# Once you have a search path, you can use pattern matching to search for samples.

# Play the 3rd sample under the 'snare' dir
s1 >> loop('snare/*', sample=2)

# You can use * in directory names too
s1 >> loop('*_120bpm/drum*/kick*')

# ** means "all recursive subdirectories". This will play the first sample
# nested under 'percussion' (e.g. 'percussion/kicks/classic/808.wav')
s1 >> loop('percussion/**/*')
