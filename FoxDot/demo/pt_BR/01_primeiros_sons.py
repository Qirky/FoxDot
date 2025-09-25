# Tutorial 1: Primeiros Sons

# No FoxDot, todas as variáveis com dois caracteres são reservadas para os objetos players, por exe,plo, 'p1'
# Criar um objeto Player sem parâmetros tocará uma única nota, C central por padrão, repetidamente até ser parada.
# Use >> para pagar um desse sons para um objeto player, por exemplo:

p1 >> pluck()

# Para parar um objeto player individual, simplismente execute

p1.stop()

# Além das variáveis de dois caractes que que são pré-reservadas, você pode criar seus
# próprios com um nome de sua escolha

foo = Player()
foo >> pluck()

# O >> no Python normalmente é reservada para um tipo de operação, como + ou -, mas isso não é o caso no caso no FoxDot.
# Se um usuário re-executar o código, FoxDot atualizará p1 instantaneamente criando um PlayerObject,
# isso quer dizer que você pode fazer mudanças na sua música  usando apenas uma linha de código.

# Agora se você passar um parâmetro para seu objeto player, você pode mudar a nota que será tocada.
# O primeiro parâmetro deve ser o grau da nota a ser tocada
# (por padrão é a nota mais baixa de 5 oitava da escala maior) e não precisa ser especificado pelo name.

# Python, como muitas linguagens de programação, usa indexação-zero quando acessado valores em um array,
# isso significa que 0 refere-se a primeira nota da escala.
# Passe para o seu objeto player instruções para fazer música com seu Synth.
# O primeiro parâmetro é a nota a da escala a ser tocada. O seguinte código
# toca as 3 primeiras notas de escala padrão (maio) repetidamente.

# Uma única nota
p1 >> pluck(0)

# Or a list of notes
# Ou uma lista de notas
p1 >> pluck([0,1,2])

# Mas, você precisa especificar qualquer outra mudança...

# Como as durações das notas, ou o tamanho de cada nota
p1 >> pluck([0,0,0], dur=[1,2,3])

# Ou a amplitude, o "volume" de cada nota
p1 >> pluck([0,0,0], amp=[1,2,3])

# Se a segunda lista, o amp, por exemplo, for mais longa, então, a primeira lista (os graus) apenas voltará ao começo, e será pareados com os elementos restantes da segunda lista (a amplitude).
p1 >> pluck([0,2,4], amp=[1,2,3,1,5])

# De modo geral, todas as listas são atravedas independente do seu tamanho
p1 >> pluck([0,2,4], dur=[1,2], amp=[1,2,3,1,5])

# Os parâmetros podem ser inteiro, ponto flutuante, fração, lista,
# tuplas, ou um misto de todos os anteriores

p1 >> pluck([0,0,0], dur=2)

p1 >> pluck([0,0,0], dur=1.743)

p1 >> pluck([0,0,0], dur=[0.25,0.5,0.75])

p1 >> pluck([0,0,0], dur=[1/4,1/2,3/4])

p1 >> pluck([0,0,0], dur=[1/4,0.25,3])

# Listas de valoers são iteradas enquanto o Player toca as notas
# A seguinte duração é igual a: 1,2,3,1,4,3
# Se você não entender isso, não se preocupe, isso será abordado com mais detalhes no tutorial sobre Padrões
p1 >> pluck([0,0,0], dur=[1,[2,4],3])

# Valores in uma tuplas são usados simultaneamente, por exemplo, p1 tocará 3 notas individuais, então, um acordes de 3 notas tocadas juntas, ao mesmo tempo.
p1 >> pluck([0,2,4,(0,2,4)])

# Você pode passar valores para os atributos do objeto player diretamente
p1.oct = 5

# Para ver todos os nomes dos atriburos do Player, apenas execute
print(Player.get_attributes())

# Um tutorial sobre os atributos do Player irá abordar o assunto com mais detalhes
 
# Você também pode armazenar diferentes players e usa-los em lugares diferentes
proxy_1 = pads([0,1,2,3], dur=1/2)
proxy_2 = pads([4,5,6,7], dur=1)

p1 >> proxy_1 # Primeiro usando o p1 

p1 >> proxy_2 # Isso troca as instruções do p1

# Para tocar varias sequencias juntas, basta fazer a mesma coisa com outro player
# Player object:

p1 >> pluck([0, 2, 3, 4], dur=1/2)

p2 >> pads([(0, 2, 4), (3, 5, 7)], dur=8)

# Toca apenas esse player, muta os outros
p1.solo() # valor padrão é 1 (solo ativo)

# E então desative o solo
p1.solo(0)

# Pare (não apenas mute) outros players
p1.only()

# Use Ctrl+. para limpar tudo que estiver agendado no relógio (parar o som de todos os players) ou execute
Clock.clear()
