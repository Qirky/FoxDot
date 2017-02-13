# TimeVar.py
---

## Classes

### var

	var.__init__(self, values, dur=4, **kwargs)

desc

	var.now(self)

desc

	var.update(self, values, dur=None, **kwargs)

desc

	var.copy(self)

desc

	var.durs(self)

desc

	var.values(self)

desc

	var.__str__(self)
	var.__int__(self)
	var.__len__(self)
	var.__float__(self)
	var.__repr.__(self)

desc

	var.__add__(self, other)
	var.__sub__(self, other)
	var.__mul__(self, other)
	var.__div__(self, other)

desc

	var.invert(self)

desc

	var.lshift(self, duration)

desc

	var.rshift(self, duration)

desc

	var.extend(self, values, dur=None)

desc

	var.shuffle(self)

desc

#### Subclasses

**Pvar**

	Pvar.__init__(self, values, dur=4)

desc

**linvar**

	linvar.__init__(self, values, dur=4)

desc

---

### const

	const.__init__(self, value)

desc

Example usage:

	>>> a = const(10)
	>>> print 1 + a
	10
	>>> print a * 4
	10


---

## Functions