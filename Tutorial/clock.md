# TempoClock.py
---

`Clock` is the main instance of `TempoClock` used in FoxDot for scheduling events but separate instances can be created and used if desired.

## Classes

### TempoClock

	TempoClock.__init__(self, bpm=120, meter=(4,4))

desc

	TempoClock.__str__(self)

desc

	TempoClock.__len__(self)

desc

	TempoClock.start(self)

desc

	TempoClock.run(self)

desc

	TempoClock.schedule(self, obj, beat=None)

desc

	TempoClock.next_bar(self)

desc

	TempoClock.bar_length(self)

desc

	TempoClock.get_bpm(self)

desc

	TempoClock.next_event(self)

desc

	TempoClock.call(self, obj, dur, arg=())

desc

	TempoClock.every(self, n, cmd, args=())

desc

	TempoClock.stop(self)

desc

	TempoClock.reset(self)

desc

	TempoClock.clear(self)

desc

### Queue

	Queue.__init__(self)

desc

	Queue.add(self, item, beat)

desc

	Queue.clear(self)

desc

	Queue.pop(self)

desc

	Queue.next(self)

desc

### QueueItem

	QueueItem.__init__(self, obj, beat)

desc

	QueueItem.__iter__(self)

desc

	QueueItem.add(self, obj)

desc

	QueueItem.call(self)

desc

### SoloPlayer

	SoloPlayer.__init__(self)

desc

	SoloPlayer.__eq__(self, other)
	SoloPlayer.__ne__(self, other)

desc

	SoloPlayer.add(self, player)

desc

	SoloPlayer.set(self, player)

desc

	SoloPlayer.reset(self)

desc

	SoloPlayer.active(self)

desc

	