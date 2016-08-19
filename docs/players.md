# Players.py

## Classes

### PlayerObject

	PlayerObject.__init__(self) 

Creates a new player object. This takes no arguments.

---

	PlayerObject.__rshift__(self, SynthDefProxy)
	PlayerObject.update(self, SynthDef, degree, **kwargs)

Two methods for updating a player's attributes. A SynthDefProxy object (see SCLang for a more in depth description) is an object that looks like a SynthDef object but acts like a PlayerObject object and passes keyword arguments and method calls to the PlayerObject it is being used with. Example:

	test = PlayerObject()
	test >> pads(dur=4)
	test.update('pads', dur=4)

---

	PlayerObject.__call__(self)

Calling a PlayerObject is what is used to send a message to SuperCollider to play a note and reschedule itself within the clock.

---

	PlayerObject.__int__(self)
	PlayerObject.__float__(self)

desc

---

	PlayerObject.__add__(self, other)
	PlayerObject.__sub__(self, other)

desc

---

	PlayerObject.rhythm(self)

desc

---

	PlayerObject.f(self, frequency)

desc

---

	PlayerObject.stutter(self, n=2)

desc

---

	PlayerObject.now(self, attr='degree', x=0)

desc

	PlayerObject.stop(self, n=0)

desc

	PlayerObject.play(self)

desc

	PlayerObject.follow(self, other, follow=True)

desc

	PlayerObject.solo(self, solo=True)

desc

	PlayerObject.lshift(self, n=1)

desc

	PlayerObject.rshift(self, n=1)

desc

	PlayerObject.reverse(self)

desc

	PlayerObject.shuffle(self, attr=None)

desc

	PlayerObject.multiply(self, n=2)

desc

	PlayerObject.every(self, n, method, args=())

desc

	PlayerObject.offbeat(self, dur=0.5)

desc

	PlayerObject.strum(self, dur=0.025)

desc

### MethodCall

	MethodCall.__init__(self, player, method, n, args=())

desc

	MethodCall.__call__(self)

desc

### Group

	Group.__init__(self, *players)

desc

	Group.__getattr__(self, name)

desc

	Group.__setattr__(self, name, value)


desc

	Group.__call__(self)

desc

	Group.play(self)

desc

	Group.stop(self)

desc
