# Tutorial 2: Manipulação Algorítimica

# O código a baixo toca as quatro primeiras notas da escala padrão repetidamente:
p1 >> pads([0,1,2,3])

# É posível manipular isso, por exemplo, adicionando uma lista de números para o objeto Player
# isso adiciona 2 graus à 4 nota tocada
p1 >> pads([0,1,2,3]) + [0,0,0,2]

# e isso adiciona 2 graus a cada 3 notas tocadas
p1 >> pads([0,1,2,3]) + [0,0,2]

# os valores também podem ser entrelaçados ou agrupados
p1 >> pads([0,1,2,3]) + [0,1,[0,(0,2)]]

# esse comportamente é particularmente útil com o método follow.
b1 >> bass([0,4,5,3], dur=2)
p1 >> pads().follow(b1) + [2,4,7]

# Você pode agendar ações para os players
# isso dirá ao p1 para inverter as notas a cada 4 batidas
p1 >> pads([0,2,4,6])
p1.every(4, "reverse")

# Você pode "encadear" o método junto do player adicionando-o ao final
# da linha original:
p1 >> pads([0,2,4,6]).every(4, "reverse")

# Para cancelar o "reverse", use o método 'never':

p1.never("reverse")

# Aqui estão alguns outros métodos que você usar:

# Usar "stutter" tocará a mesma nota 'n' vezes com diferentes atributes especificados

p1.every(4, "stutter", 4, oct=4, pan=[-1,1])

# Rotate moverá todos os valores em 1 em ordem
p1.every(4, "rotate")

# Para mudar a ordem das notas aleatóriamente, use "shuffle"
p1.every(4, "shuffle")
