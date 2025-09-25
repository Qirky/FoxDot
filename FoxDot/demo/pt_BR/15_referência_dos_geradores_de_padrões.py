# Tutorial 15: Referência Dos Geradores de Padrões


# Existem muitas classes Pattern no FoxDot para ajudar você a gerar lista de números mas também se comporta
# na mesma maneira que um Pattern base. Para ver quais padrões existem e começar a usa-los, execute
print(classes(Patterns.Sequences))



####################
# PEuclid
# PEuclid(n, k)
# Retorna o ritmo Euclidiano que espalha 'n' pulsos, quantos possíveis, dentro de 'k' passos.

# 3 pulsos dentro de 8 passos
print(PEuclid(3, 8))



####################
# PDur
# PDur(n, k, start=0, dur=0.25)
# Retorna a atual duração baseada no ritmo Euclidiano (veja PEuclid) onde dur é o tamanho de cada passo.
# Espalhe 'n' pulsos dentro de 'k' passos, quantos forem possíveis

print(PDur(3,8)) # P[0.75, 0.75, 0.5]

print(PDur(5,8))

# Dado uma lista de 3 durações, adiciona outrao com lista com 5 durações
print(PDur([3,5],8))

d1 >> play("x", dur=PDur(5,8))



####################
# PIndex
# Retorna o index acessado

print(PIndex())
print(PIndex()*4)



####################
# PSine
# PSine(n=16)
# Retorna valores de um ciclo de onda senoidal dividida em 'n' partes

# Divide em 5 partes
print(PSine(5))

# Divide em 10
print(PSine(10))



####################
# PTri
# PTri(start, stop=None, step=None)
# Retorna um Pattern equivalente à `Pattern(range(start, stop, step))` com sua forma invertida adicionada.
# Pense nisso com um "Tri"ângulo.

# Suba até 5 então desça até 1
print(PTri(5))

# Suba até 8 então desça até 1
print(PTri(8))

# Suba de 3 a 10 e então desça até 4
print(PTri(3,10))

# Suba de 3 até 30, de 2 em 2, então desça até 4
print(PTri(3,20,2))

# Suba até 4, então desça até 1, depois suba até 8, e depois desça até 1
print(PTri([4,8]))

p1 >> pluck(PTri(5), scale=Scale.default.pentatonic)

# A mesma coisa que
p1 >> pluck(PRange(5) | PRange(5,0,-1), scale=Scale.default.pentatonic)



####################
# PRand
# PRand(start, stop=None)
# Retorna um inteiro aleatório entre start e stop.

# Retorna um inteiro aleatório entre 0 e start.
print(PRand(8)[:5])

# Retorna um inteiro aleatórios entre start e stop.
print(PRand(8,16)[:5])

# Se start for um tipo de container retornará um item aleatório deste container.
print(PRand([1,2,3])[:5])

# Você pode passar uma semete
print(PRand([1,2,3], seed=5)[:5])

# Gere uma melodia aleatória
p1 >> pluck(PRand(8))

# Cria uma lista aleatória e itere pelos mesmos valores
p1 >> pluck(PRand(8)[:3])



####################
# PRhythm
# PRhythm recebe uma lista de durações únicas e tuplas com valores que podem ser fornecida ao `PDur`

# O seguinte toca o hi hat com um ritmo Euclidiano com 3 pulsos em 8 passos
d1 >> play("x-o-", dur=PRhythm([2,(3,8)]))

print(PRhythm([2, (3,8)]))



####################
# PSum
# PSum(n, total)
# Retorna um Pattern com tamaho 'n' onde cada elemento representa uma parte na soma do 'total'

# Retorna uma padrão com tamanho igual 3, onde cada elemento somado é igual a 8
print(PSum(3,8))

# Retorna um padrão com o tamanho igual 5, onde cada elemento somando é igual a 4
print(PSum(5,4))



####################
# PStep
# PStep(n, value, default=0)
# Retorna um Pattern onde cara n-termos é 'value' e o resto é o 'default'

# A cada 4, torne o valor igual 1, os outros elementos vão ser 0 por padrão 
print(PStep(4,1))

# A cada 8, use 6, o resto será 4
print(PStep(8,6,4))

# A cada 5, use 2, senão, 1
print(PStep(5,2,1))



####################
# PWalk
# PWalk(max=7, step=1, start=0)

# Por padrão , retorna um Pattern com elemento aleatoriamente 1 acima ou abaixo do anterior
print(PWalk()[:16])

# Mudando o intervalo
print(PWalk(step=2)[:16])

# Com um valor máximo
print(PWalk(max=2)[:16])

# Começe com um número diferente de 0
print(PWalk(start=6)[:16])



####################
# PWhite
# PWhite(lo=0, hi=1)
# Retorna valores aleatórios de ponto flutuante entre 'lo' e 'hi'

# 'lo' por padrão é 0, e 'hi' é 1
print(PWhite()[:8])

# Retorna números aleatórios entre 1 e 5
print(PWhite(1,5)[:8])



####################
# Geradores de Padrões Customizados

# Geradores de Pattern customizados podem ser criados usando a subclasse GeneratorPattern
# e sobrescrevendo `GeneratorPattern.func`

class CustomGeneratorPattern(GeneratorPattern):
    def func(self, index):
        return int(index / 4)

print(CustomGeneratorPattern()[:10])

# Isso pode ser feito de modo conciso usando `GeneratorPattern.from_func`,
# passando uma função que recebe um index e retorna algum item para o padrão.

def some_func(index):
    return int(index / 4)

print(GeneratorPattern.from_func(some_func)[:10])

# Podemos usar lambdas também
print(GeneratorPattern.from_func(lambda index: int(index / 4))[:10])
