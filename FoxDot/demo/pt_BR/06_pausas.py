# Tutorial 6: Pausas


# Pausas podem ser adicionadas usando um objeto rest na lista de dur
# As pausas de silêncio da nota que será "tocada".

# Sem a pausa, 5 notas (sim, dur=1 deve funcionar, mas, deixe-me explicitar um contra ponto no próximo exemplo)
p1 >> pads([0,1,2,3,4], dur=[1,1,1,1,1])

# Toque a nota 4 ... com uma pausa, a nota "4" será silenciada por 4 batidas
p1 >> pads([0,1,2,3,4], dur=[1,1,1,1,rest(4)])
