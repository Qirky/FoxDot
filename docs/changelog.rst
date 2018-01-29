Changelog
=========

v0.5.6 fixes and updates
----------------------------

* Running FoxDot with a ``--pipe`` flag is compatible with Python 2
* Updated the "pads" SynthDef
* Old unidirectional server manager class can be used by editing config file.

v0.5.5 fixes and updates
----------------------------

* Fix ``TimeVar`` class so it no longer inherits from ``Repeatable`` i.e. no longer has access to the "every" method.
* Fix pattern bug  when creating a pattern using the ``P`` generator; ``P[P(0,2)]`` no longer returns ``P[0, 2]``. However, ``P[(0,2)]`` is interpreted exactly as ``P[0, 2]`` and will return that instead.
* Added more variation to the "formantFilter" effect
* "loop" samples are added "on-the-fly" as opposed to loaded at start up. These can be loaded by filepath (with or without extension)::

    a1 >> loop("/path/to/sample.wav")
    a2 >> loop("/path/to/sample")

    a1 >> loop("yeah")             # Searches recursively for yeah.(wav|wave|aif|aiff|flac)
    a1 >> loop("perc/kick")        # Supports directories in the path
    a1 >> loop("*kick*", sample=2) # Supports * ? [chars] and [!chars]
    a1 >> loop("**/*_Em")          # Supports ** as 'recursively all subdirectories'
 
v0.5.4 fixes and updates
----------------------------

* Better communication from external processes. Running FoxDot with a ``--pipe`` flag (e.g. ``python -m FoxDot --pipe``) allows commands to be written via the stdin. Each command should end with a blank line.

v0.5.3 fixes and updates
----------------------------

* Player attribute aliases added. Using ``pitch`` and ``char`` will return a player's ``degree`` attribute.
* Player Key behaviour improved. Using multiple conditions e.g. ``4 < p1.pitch < 7`` will hold the value 1 while ``p1.pitch`` is between 4 and 7, and a 0 otherwise. These conditions can be "mapped" to values other than 1 by using the ``map`` method to map values, or results of functions, to other values/functions (which are applied to the values): ::
  
    b1 >> bass(var([0,4,5,3]))
    # Takes a dictionary of values / functions
    p1 >> pads(b1.pitch.map(
        { 0: 2,
	    4: lambda x: x + P(0,2),
		lambda x: x in (5,3): lambda y: y + PRand([0,2,4,7])
    	}))

* Known issue: mapping to a pattern of values for a Player's duration does not work as expected so be careful.
* The ``Player.every`` method can now take ``Pattern`` methods, which affect the degree of the ``Player`` (specifying attributes will be added later). Instead of applying the function every time it is called, it has a switch that applies the function then "un-applies" the function. ::

    p1 >> play("x-i-").every(6, "amen").every(8, "palindrome")

v0.5.2 fixes and updates
----------------------------

* Improved behaviour of ``TimeVar``, ``Pvar``, and ``PvarGenerator`` classes when created via mathematical operators.
* SynthDefs can be read loaded into FoxDot from SuperCollider using the ``FileSynthDef`` and ``CompiledSynthDef`` classes (see ``SynthDef.py``).
* ``DefaultServer`` instance has a ``forward`` attribute that, when not ``None``, sends any outgoing OSC message to.  Example: ::

    # Sends any OSC message going to SuperCollider to the address
    DefaultServer.forward = OSCClient(("localhost", 57890))

v0.5.0 fixes and updates
----------------------------

* Pattern "zipping" behaviour changed. A ``PGroup`` within a sequence is extended when zipped with another instead of nesting it. e.g. ::

    # Old style
    >>> P[(0,1),(2,3)].zip([(4,5)])
    P[P(0, 1, P(4, 5)), P(2, 3, P(4, 5))]
    # New style
    >>> P[(0,1),(2,3)].zip([(4,5)])
    P[P(0, 1, 4, 5), P(2, 3, 4, 5)]

* Consequently, sample player strings can use the ``<>`` arrows to play multiple sequences together using one string. ::

    # This plays three patterns together
    d1 >> play("<x ><  o[ o]>< -(-=)>", sample=(0,1,2))

* To use a different sample value for each pattern use a group of values as in the example above. Each value in relates to each pattern e.g. the "x" used sample 0, the "o" pattern uses sample 1 and the "-" pattern uses sample 2. If you want to use multiple values just use a group within a group: ::

    # Plays the snare drum in both channels at different rates
    d1 >> play("<x x><  o >", pan=(0, (-1,1)), rate=(1, (1,.9))

* Network synchronisation introduced! This is still quite a beta feature and feedback would be appreciated if you come across any issues. Here's how to do it:
 
* To connect to another instance of FoxDot over the network you need one user to be the  master clock. The master clock user needs to go from the menu to "Language" then "Listen  for connections". This will start listening for connections from other FoxDot instances. It will print the IP address and port number to the console; give this information to your live coding partner. They need to run the following code using the IP address on the master clock machine: ::

    Clock.connect("<ip address>")

* This will copy some data, e.g. tempo, from the master clock and also adjust for the differences in local machine time (if your clocks are out of sync). The latter will depend on the latency of the connection between your machines. If you are out of time slightly, set the ``Clock.nudge`` value to a small value (+-0.01) until the clocks are in sync. Now whenever you change the ``Clock.bpm`` value, the change will propagate to everyone on the next bar. 


v0.4.14 fixes and updates
-----------------------------

* Pattern getitem method now allows Patterns to be indexed using a Player Key e.g. ``P[0,1,2,3][p1.degree]`` that will return the item in the Pattern based on the  integer values of the key (``p1.degree`` in this example).
* Added ``future`` method. Like ``schedule`` it adds a callable object to the queue but doesn't need the exact beat occurrence, just how many beats in the future from "now". First argument is time, followed by the object, arguments, and keyword arguments.
* Player object ``stop`` method properly removes the player from ``Clock.playing`` list.
* Using Player Key ``__getitem__`` returns a player key whose calculation function is ``__getitem__``. This is useful if you want to use just one of the values of another player if they are in a group. e.g. ::

    p1 >> pads((0,2,4) + var([0,4,5,3]))
    b1 >> bass(p1.degree[0]) # Only plays the "root" note of the chord

* SuperCollider bus number resets to 4 instead of 1 to prevent feedback loops when using reverb.
* Changed "verb" keyword to "mix" for reverb effect. Default is changed from 0.25 to 0.1.
* ``GeneratorPattern`` ``new`` method converts the  ``other`` argument to a Pattern so you can use lists/tuples as opposed to just Patterns/PGroups when performing operations e.g. ``PWalk() + (0,4)``.
* Fixed ``newline`` method to only add an indent if the INSERT index was in brackets or following a colon instead of doing so if the line had open brackets / colon. Evaluated code no longer highlights any empty preceeding lines.
* Python 3 uses xrange as range

v0.4.13 fixes and updates
-----------------------------

* Moved demo files into main package to fix install from pip.

v0.4.12 fixes and updates
-----------------------------

* ``Player.stop_calling`` is now ``Player.never``. If a ``Player`` is calling its own method (implemented by the ``every`` method e.g. ``p1 >> pads().every(4, "reverse")`` you can now stop the repeated call by using ``p1.never("reverse")``.
* Fixed circular referencing bug when using PGroups e.g. ``p1 >> pads(p1.degree + (0,4))``
* Window transparency can now be toggled from the "Edit" menu
* Added Tutorial files that can be loaded from the menu
* Multiple uses of the ``every`` method with the same method name can be used together by specifying an ``ident`` keyword, which can be any hashable value i.e. a string or integer. ::

    # The second "stutter" no longer overrides the first
    d1 >> play("x-u-").every(8, "stutter", 8).every(3, "stutter", 4, dur=1, degree="y", ident=1)

* Fix ``group_modi`` function to test for ``TimeVar`` instances instead of trying and failing to index their contents so that ``TimeVar``'s with strings in their contents don't get into an infinite recursive call. 

v0.4.11 fixes and updates
-----------------------------

* Removed ``sys.maxint`` to conform with Python 3

v0.4.10 fixes and updates
-----------------------------

* Fixed negative pitch bug
* ``PGroupMod`` replaces ``PGroupStar`` when using square brackets in a "play" string. This "flattens" the values so that many nested ``PGroups`` don't create exponentially larger loops when sending events to SuperCollider.
* Fixed ``stutter`` so that delays caused by ``PGroups`` are no longer lost.
* ``PRand``, ``PwRand``, and ``PxRand`` choose from a random index instead of a random element so that any "nested" ``GeneratorPatterns`` generate a new item instead of returning the same one i.e. at index 0.
* Fixed ``Player.degrade``
* ``slidedelay`` default value changed from 0.75 to 0
* Replaced "Control" with "Command" for menu short-cuts on Mac OS (Thanks ianb) 
* Improved documentation layout
* Player methods such ``shuffle`` no longer affect the text of a ``play`` Player as it would overload the undo heap. This may be added back in at a layer date.
* Infinite recursion errors caused by circular referencing no longer seem to occur.
* Improved printing of Players to include identifier e.g. ``<p1 - pluck>``.
 
v0.4.9 fixes and updates
----------------------------

* Fixed issues with indexing ``GeneratorPattern`` and using ``var`` in Player methods.
* Random ``GeneratorPattern`` objects, such as ``PRand`` can take a ``seed`` keyword that will give you the same sequence of values for the same value of seed (must be an integer).

v0.4.8 fixes and updates
----------------------------

* Unsaved work is stored in a temporary filed that can be loaded on the next startup.
* Player objects can now take tuples as an argument, which delays the next event (similar to the ``delay`` argument but works with the following event)::

    # The Player object uses the smallest duration in the tuple to move to the next event
    p1 >> pluck([0,1,2], dur=[1,1,(0.5,1)])

* Pattern function ``PRhythm`` takes a list of single durations and tuples that contain values that can be supplied to the ``PDur`` e.g.::

    # The following plays the hi hat with a Euclidean Rhythm of 3 pulses in 8 steps
    d1 >> play("x-o-", dur=PRhythm([2,(3,8)]))

v0.4.7 fixes and updates
----------------------------

* FoxDot is now Python 3 compatible, so make sure you treat your print statements as functions i.e. use ``print("Hello, World!")``
* Added ``audioin`` SynthDef for processing audio from the default recording device.
* Fixed bugs relating to chaining multiple ``every`` methods and ending their call cycle when the parent player is stopped
* Improved flexibility of referencing player attributes e.g. ::

    p1 >> pads([0,1,2,3], dur=2).every(8, "stutter", 4, degree=p1.degree+[2,4,7])

v0.4 fixes and updates
--------------------------

* FoxDot is now Python 3 compatible, so make sure you treat your print statements as functions i.e. use ``print("Hello, World!")``
 
v0.3.7 fixes and updates
----------------------------

* Nested pattern bug fixed so that they no longer cause patterns to loop
* Improved clock scheduling after proper "latency" implementation
* Added a new SynthDef, ``loop``, to play longer samples: ::

    # First argument is the name of the file minus the extension
    
    p1 >> loop("billions")
    
    # Use the dur keyword to specify when to loop the file
    
    p1 >> loop("billions", dur=8)
    
    # The second argument is the starting point in beats such that the following 2 lines are equivalent
    
    p1 >> loop("billions", dur=16)
    
    p1 >> loop("billions", [0,8], dur=8)

* Added ability to use the lambda symbol in place of the word lambda. Insert it by using ``Ctrl+L``.
* Put ``slide``, ``slidefrom``, ``coarse``, ``pshift`` into their own effects

v0.3.6 fixes and updates
----------------------------

* Any delay or stutter behaviour in Players is now handed over to SuperCollider by timestamping the OSCBundle, which should make FoxDot a lot more efficient & removed ``send_delay`` and ``func_delay`` classes.
* Using a ``TimeVar`` in a pattern function, such as ``PDur``, now creates a time-varying pattern as opposed to a pattern that uses the ``TimeVar``'s current value. e.g. ::

    >>> test = PDur(var([3,5], 4), 8)
    >>> print test # time is 0
    P[0.75, 0.75, 0.5]
    >>> print test # time is 4
    P[0.5, 0.25, 0.5, 0.25, 0.5]

* Adding values to a player performs the whole operation as opposed to adding each value in turn when the Player is called. This improves efficiency when using data structures such as ``TimeVar``s as it only creates a new once ``TimeVar`` when the addition is done.
* Improved usability of ``PlayerKey`` class, accessed when get the attribute of a Player e.g. ``p1.degree``.
* Sleep time set to small value. 0 sleep time would crash FoxDot on startup on some systems.
* Made the behaviour of the ``every`` method more consistent rather than just starting the cycle at the next bar.

v0.3.5 fixes and updates
----------------------------

* In addition to P\*, P+, P/, and P\** have been added. P+ refers uses the sustain values in a player to derive its delay. P/ delays the events every other time it is accessed, and P\** shuffles the order the values are delayed.
* Added ``PWalk`` generator pattern. 
* TimeVars are easier to update once created. ::

    # Creates a named instance called foo
    var.foo = var([0,1],4)
    
    # Reassigning a var to a named var updates the values instead of creating a new var
    var.foo = var([2,3,4,5],2)

* Removed ``sleep`` from scheduling clock loop to increase performance. If you want to decrease the amount of CPU FoxDot uses, change the sleep duration to a small number around 0.001 like so ::

    Clock.sleep_time = 0.001

* Added pitch shift (``pshift``) to Sample Players, which increases the pitch of a sample by the number of semitones. You can use ``Scale.default.semitones()`` to generate semitones from the current scale.

v0.3.3 fixes and updates
----------------------------

* Added a new ``Pattern`` type data structure called a P-Star or ``P*``. It is a subclass of ``PGroup`` but it has a "behaviour" that effects the current event of Player object, which, in this instance, adds a delay to each value based on the current Player's duration. e.g. ::

    # Plays the first note, 0, for 4 beats then the pitches 2, 4, and 6 at 4/3 beats each.
    p1 >> pluck([0, P*(2,4,6)], dur=4)
    
    # The can be nested
    p1 >> pluck([0, P*(2,4,P*(6,7)], dur=4)
    
    # Work in the same way that a SamplePlayer uses square brackets
    p2 >> play("x[--]o[-o]")

* Frequency and buffer number calculation is done per OSCmessage which means these values can be modified in any delayed message i.e. when using the Player ``stutter`` method like so: ::

    p1 >> pluck([0,1,2,3], dur=1).every(4, 'stutter', 4, degree=[10,12], pan=[-1,1] )
    
    d1 >> play("x-o-").every(5, 'stutter', 2, cycle=8, degree="S")

* Using as ``linvar`` as the Clock tempo will no longer crash the Clock.
* New effects have been added; ``shape`` which is a value between 0 and 1 (can be higher) that relates to a level of distortion, and ``formant`` which is a value between 0 and 8 and applies different formant filters to the  audio.
* ``hpf`` and ``lpf`` have resonance values now: ``hpr`` and ``lpr``
* You can open the config file directly from FoxDot by using the "Help & Settings" menu. Likewise you can open the directory that holds where your samples are kept. This can be changed in the config file.

v0.3.2 fixes and updates
----------------------------

* ``PlayerKey`` data type can handle ``PGroup`` transformations without crashing, which improves performance when using ``follow``
* ``PlayerKey`` data type greater than and less than functions fixed and now works with amplitudes.
* Better handling of scheduled functions that are "late"
* Experimental: ``play`` SynthDef can have a rate of -1 to be played in reverse and also uses a keyword ``coarse`` similar in function to ``chop``
* Added ``Pattern`` method, palindrome that appends a mirrored version of the pattern to itself.
* Removed visual feedback for shuffling, rotating, etc patterns in Players as it did not work correctly with nested patterns.

v0.3.1 fixes and updates
----------------------------

* ``TempoClock`` uses a ``start_time`` value that, when used on multiple instances of FoxDot, should synchronise the timings. This is a work in progress
* Added a "use SC3 Plugins" tick-box on the "Code" drop down menu to allow for easier configuration
* ``piano`` SynthDef added using th SC3 Plugin "MdaPiano"

v0.3 fixes and update
-------------------------

* ``var`` type can be used with Player ``delay`` and nested groups in the ``oct`` attribute.
* Increased ``TempoClock`` latency to 0.2 seconds for improved performance.
* Better handling for auto-completed quotation marks 

v0.2.11 fixes and updates
-----------------------------

* Caught ``ImportError`` if the user does not have ``rtmidi`` installed.
* Improved ``Player.stutter``

v0.2.10 fixes and updates
-----------------------------

* New SynthDefs added. Use ``print SynthDefs`` to view.
* Improved timing in the ``TempoClock`` class through use of threading and a latency value. Thanks to Yaxu and Charlie Roberts for the help.
* Dubstep samples added to the 'K' character. 
* Sample banks re-arranged. Use ``print Samples`` for more information.
* Sample Player argument, ``scrub`` removed. You can now use ``slide``/``slidefrom`` and ``vib`` as you would do with a normal Player object to manipulate playback rate.
* ``Pattern`` class now has a ``layer`` method that takes a name of a ``Pattern`` method as its first argument and then arguments and keyword arguments for that method and creates a pattern of ``PGroups`` with their values zipped together. ::

    >>>  print P[1,2,3,4].layer("reverse")
    P[P(1, 4), P(2, 3), P(3, 2), P(4, 1)]

    >>>  print P[1,2,3,4].layer("rotate", 2)
    P[P(1, 3), P(2, 4), P(3, 1), P(4, 2)]
 
* New nested ``PGroup`` behaviour added for players. Each value in each ``PGroup`` in an event relates to the values in any other ``PGroup`` in the same index, even if that value is also a ``PGroup``. This concept is better described through an example: ::

    p1 >> pluck((0,2), pan=(0,(-1,1)), vib=(0,(0,12)), dur=4, chop=(0,4))

* The first note, 0, is played with a pan of 0, chop of 0, and with no vibrator added. The second note, 2, is played with a chop of 4 and with no vibrato with a pan of -1 (left) but with a vibrato value of 12 with a pan of 1 (right). 

* Experimental: Players can "follow" other Players' attributes over time by referencing their attributes. ::

    p1 >> pads([4,5,6,7], dur=2, chop=4)

    p2 >> pluck(p1.degree + 2, vib=p1.chop*3)

v0.2.9 fixes and updates
----------------------------

* Improved automatic bracket handling and formatting
* Colour scheme update
* "Upper-case" samples now read properly
* ``cycle`` argument added to the ``.every()`` player method to denote the cycle length of which to execute the specified method, e.g. ::

    # Shuffles the samples on the 5th beat of each 8 beat cycle
    bd >> play("x-o-").every(5, 'shuffle', cycle=8)

v0.2.8 fixes and updates
----------------------------

* Minor bug fixes
* Improved automatic bracket handling and formatting
* Console is now resizable
* Scale and root can be assigned using the equals operator e.g. ``Scale.default = "minor"`` and ``Root.default = var([0,4])``

v0.2.7 fixes and updates
----------------------------

* Rest class added
* Undo and Redo functions fixed
* Infinite loop caused by empty brackets in PlayStrings fixed
* Menu bar added with several short-cuts
* Player follow method improved
* Improved documentation
* "style" keyword argument changed to "sample"

v0.2.6 fixes and updates
----------------------------

* OSC Communication is now done through a dedicated SuperCollider Quark

v0.2.3 fixes and updates
----------------------------

* Effects are now implemented using busses on SuperCollider, which uses less CPU 
* Effects can be customised and defined
* Sample Player behaviour (i.e. how the string of characters relates to playback) has been altered. Square brackets refer to a single event even though two samples are played.
* SuperCollider is booted on startup with a compiled startup file.

v0.2.2 fixes and updates
----------------------------

* ``PDur`` added: a pattern that implements Euclidean Rhythms
* Player attributes can be manipulated using the ``Player.every`` method
* Errors caught and displayed in FoxDot console instead of crashing
* Can set different tempi for Players using the ``bpm`` keyword 
* Sample Player objects can play multiple samples together by grouping them as a PGroup but cannot feature square brackets

v0.2.1 fixes and updates
----------------------------

* Syntax highlighting bugs fixed
* Visual feedback for ``shuffle``, ``mirror``, and ``rotate`` methods for ``play`` SynthDef
* SC3 Plugins disabled by default
* Player Object dictionaries shallow copied before iteration to stop ``RunTimeErrors`` occurring 

v0.2.0 fixes and updates (4/12/16)
--------------------------------------

* Reorganised project structure. Samples and code are kept separate.
* SuperCollider ``OSCFunc.scd`` now found in ``/osc/`` folder
* ``setup.py`` now included for an easier install
* (in progress) characters can have more than one sample attached to them. These are accessed by supplying a ``buf`` keyword argument.  
* Python lists can be interpreted as FoxDot pattern when attached with a P prefix e.g. ``P[1, 2, 3] + [0,2]`` will return ``P[1,4,3,3,2,5]`` not ``[1,2,3,0,2]``.

v0.1.9 fixes and updates
----------------------------

* PSparse renamed to PBin
* Loading the icon now works on Linux
* Upheaval of SCLang API
* Player Objects now have visual feedback behaviour via the ``bang`` method and take Tkinter tag_config keyword arguments.
* Consolas now default font
* Fixed ``Pvar`` and ``linvar`` bugs

v0.1.8 fixes and updates
----------------------------

* PSparse pattern type added (all Pattern names can be seen by executing ``print(PatternTypes)``
* Major overhaul of Pattern nesting/lacing behaviour. Patterns can now be nested to multiple levels.
* Player object attributes now 'follow' one another and their current  values are examined instead of the Pattern value

v0.1.7 fixes and updates
----------------------------

* "Chop" added to default SynthDef behaviour
* GUI icon updated
* Using ``var`` objects for Player durations no longer crashes
* New Pattern types added
* FoxDot can be run using ``python -m FoxDot`` if FoxDot is in your PATH

v0.1.6 fixes and updates
----------------------------

* Decimator (a.k.a. bitcrush) added to default SynthDef behaviour
* ``SynthDefs`` and ``BufferManager`` can be reloaded
* Removed automatic bootup of sclang as default behaviour
* Added new SynthDefs

v0.1.5 fixes and updates
----------------------------

* Removed RegEx find and replace ``>>`` and ``$`` syntax. FoxDot now uses pure Python code and saved files can be run by themselves.

v0.1.4 fixes and updates
----------------------------

* Save/Open file feature added
* Console can now be toggled
* Reduced CPU usage when the TempoClock queue is empty
* Added a 'grain' attribute to the ``sample_player`` SynthDef

v0.1.3 fixes and updates
----------------------------

* Key bindings for Linux, Mac, and Windows 10 fixed
* Fixed freeze on keyboard interrupt exit
