# C:/Users/Ryan/Desktop/test.py
from __future__ import division
from FoxDot import *

@livefunction
def partA():
    a1 >> dab(dur=32, sus=8, amp=[1])
    a2 >> varsaw(Prand(5), dur=8, sus=14, amp=1/2, rate=Prange(8)/8, scale=Scale.default.pentatonic)
    a3 >> pads(amp=0)                                                               
    l1 >> pluck(var([0,-1]) + (0,9), dur=Pvar([Psum(5,4),1/4],[24,8])) + var([0,[1,-1,-1,2]],[7,1])
    d1 >> play("x^", lpf=400, dur=PSum(6,4), rate=1/2)
    d3 >> play("m  m  m ", rate=(.9,1))
    d4 >> play("o[oo]", amp=linvar([0,2],[32,0]), amplify=var([1,0],[28,4]))
    
p >> pads()


@livefunction
def partB():
    chords = var([0,2,3],[4,2,2])
    a3 >> pads([0,4,7], amp=var([0,1/2],16), dur=1/4, bits=2, oct=[5,5,5,6], blur=1.5) + [0,0,2,0,0]
    a1 >> zap(chords, dur=Psum(7,4), sus=1, oct=5, blur=2, delay=Pstutter([0,(0,.2,.4)],[[4,5,1],1])) + (0,2,4,const(6))
    d1 >> play("X-", lpf=20000, dur=1/2, rate=1)
    d3 >> play(" ( ( O))O( ( [( O)O]))", sus=0.1)
    d2 >> play("H", amp=Prand([1,0])[:8], room=0.5)
    l1 >> saw(var([3,2,1,2,1,-1,-2],[1,1,1,.5,.5,2,2]), dur=[1,1,1,.5,.5,2,2], vib=10, oct=6) + var([0,4,[2,9]],[12,2,2])
    d4.amplify=0    

Root.default.set(var([-4,0],64))
    
print Clock.when_statements

p >> pads()

print t
    
t = var([0,1],32)

when(lambda: t== 1).do(partA).elsedo(partB)
