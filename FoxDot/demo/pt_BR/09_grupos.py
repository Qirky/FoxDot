# Tutorial 9: Grupos


# Os atributos dos players, com degree ou scale, podem ser alterados atribuindo-lhes o valor diretamente, então, isto aqui
p1 >> pads([0,2,4,2], scale=Scale.majorPentatonic)

# seria equivalente a
p1 >> pads()
p1.degree = [0,2,4,2]
p1.scale = Scale.majorPentatonic

# Isso é muito útil se você quiser usar o mesmo valor para múltiplos Players simultaneament, por exemlo:
p1 >> pads([0,2,4,2])
p2 >> pads([2,1,0,4])
p3 >> pads([2,3])
p1.dur=p2.dur=p3.dur=[1,1/2,1/4,1/4]

p1.stop()
p2.stop()
p3.stop()

# Você também pode referênciar todos os membros que o nome começam com a mesma letra
p_all.dur = [1/2,1/4] # Roda para p1, p2, etc, que estiverem tocando!

# ou
p_all.amplify = 1

# ou...
p_all.stop()

# ou...
p_all.solo()

# Para reduzir um pouco a digitação, os players podem ser agrupados juntos, assim, modificar os atributos é bem simple:
p1 >> pads([0,2,4,2])
p2 >> pads([2,1,0,4])
p3 >> pads([2,3])
g1 = Group(p1, p2, p3)
g1.dur=[1,1/2,1/4,1/4]

# Você também pode agrupas com os grupos _all
g1 = Group(p_all, d_all, b1, b2)

# Defina um volume por 4 batidas, e depois altera ele por mais 4
# Isso sobreescreve amplitudes definidas em seus players
g1.amp=var([1,0],4)

g1.stop()

# Você pode usar funções para agrupar coisas juntas. Para executar use CTRL+Enter, não ALT+Enter.
def tune():
    b1 >> bass([0,3], dur=4)
    p1 >> pluck([0,4], dur=1/2)
    d1 >> play("x--x--x-")
tune()

# Ou agende no relógio a chamada da função agrupadora
def verse():
    b1 >> bass([0,3], dur=4)
    p1 >> pluck([0,4], dur=1/2)
    d1 >> play("x--x--x-")
    Clock.future(16, chorus)
def chorus():
    b1 >> bass([0,4,5,3], dur=4)
    p1 >> pluck([0,4,7,9], dur=1/4)
    d1 >> play("x-o-")
    Clock.future(16, verse)
verse()

