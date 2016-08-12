from FoxDot import *
b >> bass(var([0,4,5,3]), dur=1/2, sus=1) + var([0,[1,-1]],[3,1])

p >> pads(var([0,4,5,3])) + (0,2,4)

bd >> play("x-o-")
