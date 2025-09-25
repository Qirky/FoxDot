# Tutorial 4: Usando Padrões


# Objetos Player usam listas Python, algo próximo a arrays em outras linguagens,
# para as suas sequências. Você já usou elas anteriormente, mas, elas não são exatamente
# flexiveis para manipular. Por exemplo, tente multiplicar a lista por dois, algo como:

print([1, 2, 3] * 2)

# Esse é o resultado que você esperava?

# FoxDot usa um tipo de container chamado 'Pattern' para ajudar a resolver esse problema.
# Ele atua parecido com uma lista comum, mas, qualquer operação matemática é feita em cada item
# da lista e feito por pares se usado um segundo padrão. Um padrão básico é criado como
# você criaria uma lista ou tupla normal, mas com um 'P' antes.

print(P[1,2,3] * 2)

print(P[1,2,3] + 100)

# Nessa operação, a saida consiste em todas as combinações dos dois padrões, algo como:
# [1+3, 2+4, 3+3, 1+4, 2+3, 3+4]
print(P[1,2,3] + [3,4])

# Você pode usar a sintaxe de fatiamento do Python para gerar uma série de números

print(P[:8])

print(P[0,1,2,3:20])

print(P[2:15:3])

# Tente alguma outra operação matemática e veja qual é o resultado obtido.
print(P[1,2,3] * (1,2))

# Objetos Pattern também são automaticamente entrelaçados com qualquer lista aninhada.
# Compare
# Lista normal:
for n in [0,1,2,[3,4],5]:
    print(n)

# com
# Pattern
for n in P[0,1,2,[3,4],5]:
    print(n)

# Use PGroups se você quiser evitar esse comportamento. Isso tanbém pode ser feito
# usando tuplas no Patterns:
for n in P[0,1,2,(3,4)]:
    print(n)

# Isso é um PGroup:
print(P(0,2,4) + 2)

print(type(P(0,2,4) + 2))

# Em Python, você pode gerar um intervalo de inteiro com a sintaxe range(start, stop, step).
# Por padrão, start é 0 e step e 1.
print(list(range(10))) # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Você pode usar PRange(start, stop, step) para criar um objeto Pattern com os valores equivalentes:
print(PRange(10)) # P[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# P[0, 2, 2, 6, 4, 10, 6, 14, 8, 18]
# [0*1, 1*2, 2*1, 3*2, 4*1, 5*2, 6*1, 7*2, 8*1...]
print(PRange(10) * [1, 2])           # comportamento da classe Pattern

# Adicionar uma lista (ou Pattern) a um Pattern irá adicionar os valores dos
# elementos um para o outro, onde listas Python seriam concatenatedas.
print(PRange(10) + [0,10])

# Para concatenar Patterns, use o operador pipe, como:
print(PRange(10) | [0,10])
# FoxDot converte automaticamente qualquer objeto entre o pipe, que envolva um Pattern, em uma classe base Pattern
# então, você não precisa se preocupar em criar em os tipos.

# Toca todos os valores juntos
p1 >> pluck(P(4,6,8))
p1 >> pluck(P[0,1,2,P(4,6,8),7,8])

# Espalhe os valores entre o "dur", por exemplo, se o dur for 2 batidas, então, irá tocar cada valor em 2/3 batidas
p1 >> pluck(P*(0,2,4), dur=1/2)
p1 >> pluck(P*(0,2,4), dur=1)
p1 >> pluck(P*(0,2,4), dur=2)
p1 >> pluck(P[0,1,2,P*(4,6,8),7,8], dur=1)

# Isso é o mesmo que P*, mas todas as vezes as notas são reproduzidas e elas são espalhadas pelo valor do dur.
p1 >> pluck(P/(0,2,4), dur=1/2)
p1 >> pluck(P/(0,2,4), dur=1)
p1 >> pluck(P/(0,2,4), dur=2)
p1 >> pluck(P[0,1,2,P/(4,6,8),7,8], dur=1)

# Espalhe os valores pelo "sus" atual, por exemplo, se o dur for 2 batidas e o sus for 3 batidas, então, será tocado cada valor 1 batida a parte.
p1 >> pluck(P+(0,2,4), dur=2, sus=3)
p1 >> pluck(P+(0,2,4), dur=2, sus=1)
p1 >> pluck(P[0,1,2,P+(4,6,8),7,8], dur=1, sus=3)

# Espalhe os primeiros (tamanho - 1) valores com um intervalo com o último valor entre cada um
# Toque 0,2,4 com um intervalo de 0.5:
p1 >> pluck(P^(0,2,4,0.5), dur=1/2)

# Os padrões tem vários métodos para manipular os conteúdos
help(Pattern)

# Padrão simples
print(P[:8])

# Emparalhe o padrão para criar aleatoriedade
print(P[:8].shuffle())

# Adicione um padrão invertido ao padrão
print(P[:8].palindrome())

# Rode o padrão por n (padrão 1)
print(P[:8].rotate())
print(P[:8].rotate(3))
print(P[:8].rotate(-3))

# Pegue o padrão e adicione ele quantas vezes precisar até que o números de elementos seja igual ao desejado em um novo padrão
print(P[:8].stretch(12))
print(P[:8].stretch(20))

# Inverta um padrão
print(P[:8].reverse())

# Repita o padrão n vezes
print(P[:8].loop(2))

# Adiciona um deslocamento somado
print(P[:8].offadd(5))

# Adiciona um deslocamento multiplicado
print(P[:8].offmul(5))

# Stutter - Repete cada elemento n vezes
print(P[:8].stutter(5))

# Amen
# Combina e une o primeiro e os dois últimos itens, de modo que um
# padrão de bateria "x-o-" se tornaria "(x[xo])-o([-o]-)" e imita
# o famoso ritmo "amen break"
d1 >> play(P["x-o-"].amen())
print(P[:8].amen())

# Bubble
# Combina e une o primeiro e os dois últimos itens, de modo que um
# padrão de bateria "x-o-" se tornaria "(x[xo])-o([-o]-)"
d1 >> play(P["x-o-"].bubble())
print(P[:8].bubble())

