# Tutorial 10: Usando Variáveis Dependente Do Tempo


# Um TimeVar é uma abreviação para "Time Dependent Variable" (Variável Dependente Do Tempo) e é uma funcionalidade chave para o FoxDot.
# Um TimeVar tem uma série de valores que devem mudar depois de um número de batidas pré definidas
# e isso é criado usando um objeto var com a sintaxe var([lista_de_valores],[lista_de_durações]).

# Gera os valores: 0,0,0,0,3,3,3,3...
a = var([0,3],4)            # Duração pode ser um único valor
print(int(Clock.now()), a)  # 'a' inicializa com o valor 0
# >>> 0 0                   # O primeiro valor de ser diferente...

print(int(Clock.now()), a)   # Depois de 4 batidos o valor muda para 3
# >>> 4 3

print(int(Clock.now()), a)   # Depois de outras 4 batidas, o valor muda para 0
# >>> 8 0

# Duração também pode ser uma lista
a = var([0,3],[4,2])
print(int(Clock.now()), a)

# Quando um TimeVar é usado em uma operação matemática, o valor também se torna um TimeVars
# que muda o estado quando o TimeVar original mudar – isso pode ser feito com padrões também
a = var([0,3], 4)
print(int(Clock.now()), a + 5)   # Quando a batida é 0, a é 5
# >>> 0 5

print(int(Clock.now()), a + 5)   # Quando a batida é 4, a é 8
# >>> 4 8

b = PRange(4) + a
print(int(Clock.now()), b)   # Depois de 8 batidas, o valor muda para 0
# >>> 8 P[0, 1, 2, 3]

print(int(Clock.now()), b)   # Depois de 12 batidas, o valor muda par 3
# >>> 12 P[3, 4, 5, 6]

# Use 'var' com seu Player para criar uma progrssão de acordes.
a = var([0,4,5,3], 4)
b1 >> bass(a, dur=PDur(3,8))
p1 >> pads(a + (0,2), dur=PDur(7,16))

# Você pode adicionar um 'var' a um Player ou um var.
b1 >> bass(a, dur=PDur(3,8)) + var([0,1],[3,1])

b = a + var([0,10],8)

print(int(Clock.now()), (a, b))

# Atualizar os valores de um 'var' irá mudar em todos os lugares
a.update([1,4], 8)

print(int(Clock.now()), (a, b))

# Vars podem ser nomeadas ...
var.chords = var([0,4,5,4],4)

# E usadas depois
b1 >> pluck(var.chords)

# Qualquer players usando a var nomeda será atualzado
var.chords = var([0,1,5,3],4)

# Você pode usar um 'linvar' para criar mudanças nos valores gradativamente durante o tempo
# Varie o valor de 0 a 1 durante 16 batidas
c = linvar([0,1],16)

# Rode isso várias vezes e veja a mudança acontecer
print(int(Clock.now()), c)

# Varie o amp baseado nesse linvar
p1 >> pads(a, amp=c)

# um 'Pvar' é um 'var' que pode armazenar padrões (em oposição a dizer, números inteiros)
d = Pvar([P[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], P[0, 1, 2, 3, 4, 5, 4, 3, 2, 1]], 8)

print(int(Clock.now()), d)

p1 >> pads(a, amp=c, dur=1/4) + d

# Mude a escala a cada 16 batidas
Scale.default = Pvar([Scale.major, Scale.minor],16)

# Você também pode definir um valor para durar para sempre quando for alcançado usando um valor especial chamado "inf"

x = var([0, 1, 2, 3], [4, 4, 4, inf])

print(x) # Manteha pressionado - eventualmente irá para no 3

######################
# Outros tipos de "var"

# Aqui está uma lista de sub-classes de "var" que retornam valores entre
# os números especificados. Por exemplo, um "linvar" muda gradualmente
# os valores modo linear:

print(linvar([0,1],8)) # matenha rodando para ver o valor alterar entre 0 e 1

# Exemplo: aumente o corte do filtro passa-altas em 32 batidas

p1 >> play("x-o-", hpf=linvar([0,4000],[32,0]))

# Outros tipos incluem "sinvar" e "expvar"

print("Linear:", linvar([0, 1], 8))
print("Sinusoidal:", sinvar([0, 1], 8))
print("Exponential:", expvar([0, 1], 8))

#################
# Pattern TimeVar

# As vezes nós queremos armazenar um padrão inteiro em um var, mas
# se tertarmos isso, ele seram entrelaçados automaticamente:

pattern1 = P[0, 1, 2, 3]
pattern2 = P[4, 5, 6, 7]

print(var([pattern1, pattern2], 4))

# Para armazenar o todo padrão você precisa usar um "Pvar", que não
# entrelaça os valores, mas guarda os padrões em seu lugar

print(Pvar([pattern1, pattern2], 4))

p1 >> pluck(Pvar([pattern1, pattern2], 4), dur=1/4)



###########################
# Compensando o horário de início

# Um outro truque bem útil é compensar o tempo de início para o var. Por
# padrão isso é feito quando o tempo do relógio é 0 mas você pode especificar um valor
# diferente usando o parâmetro "start"

print(linvar([0, 1], 8))
print(linvar([0, 1], 8, start=2))

# Isso pode ser combinado com Clock.mod() para iniciar uma rampa no início do
# próximo ciclo de 32 batidas:

d1 >> play("x-o-", hpf=linvar([0,4000],[32,inf], start=Clock.mod(32)))
