from __future__ import division
from FoxDot import *
# --- Made with FoxDot --- #

Scale.default.set("minor")
Root.default.set(var([0,4],64))
Clock.bpm=105

bd >> play("X", amp=Prand([1/2,0])[:8], bits=2, rate=var([1,2]), pan=0)

ch >> charm((0,2,4), amp=1/8, delay=(0,0.05,0.1)).offbeat() + var([0,-1,3,2])

sn >> play(" ( ( (I[Im])))I ", rate=(.9,1), pan=(-1,1), amp=1, sus=0.1)
bb >> play("X-")

hh >> play("~", dur=var([1/2,1/4],[4,2,3,1]))

cp >> play("*[*]", amp=Prand([1,0])[:8], room=0.5, rate=5)

Group(bb,bd,sn).hpf=var([0,4000],[28,4])

d2 >> dirt(var([0,var([2,6],[12,4])],[3,1]), amp=Prand([1,0])[:16] * 2, dur=1/4) + var([0,3],[24,8])

v1 >> varsaw(0, dur=1/4, amp=1/2, rate=linvar([0,1],12), hpf=linvar([0,5000],28))
