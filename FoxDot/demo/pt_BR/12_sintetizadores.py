# Tutoral 12: Sintetizadores


# O FoxDot cria música dando um 'instrumento digital' para um objeto player
# para tocar, que são chamados de 'SynthDefs'. Você pode ver a lista de 'Synths'
# pré-instalados executando

print(SynthDefs)

# Cara um desses representa um *objeto* `SynthDef`. Esses objetos são
# dados ao Players para ser tocado - como dar um instrumento para alguem de sua
# orquestra.

# Escrevendo suas próprias Definições de Sintetizador

# Isso é um pouco mais avançado, mas se você já escreveu SynthDefs no
# Supercollider, você se sentirá em casa. Senão, volte para esta esção mais
# tarde.

# O FoxDot pode acessar qualquer SynthDef armazenado no servidor do SuperCollider,
# mas, você precisa saber que ele está lá. Se você já escreveu um SynthDef
# no SuperCollider e nomeou ele com \mySynth, então, você pode criar uma instância de um
# SynthDef no FoxDot, por exemplo:

mySynth = SynthDef("mySynth")

# Usar o mesmo nome para o seu SynthDef no FoxDot e SuperCollider
# é uma boa ideia para evitar confusões. Se você quer escrever (ou editar) o seu
# SynthDef durante o tempo de execução no FoxDot você pode usar uma API SuperCollider
# importando o módulo SCLang. Todos os SynthDef no FoxDot herdam o comportamento
# da classe-base, como, por exemplo, os filtros passa-baixo/alto e vibrato,
# mas isso pode ser sobreescrito ou atualizado fácilmente. Se você quiser saber mais
# about digital sound processing and SynthDef creation, check out the
# veja a documentação do SuperCollider. Abaixo está um exemplo da criação no FoxDot:

# Importe o módulo para escrever código SCLang no Python
from FoxDot.lib.SCLang import *

# Crie um SynthDef nomeado como 'example' (usar o mesmo nome para a variáble e para o SynthDef é uma boa ideia)
example = SynthDef("example")

# Crie o oscilador (osc) usando um sinal de onda
example.osc = SinOsc.ar(ex.freq)

# E adicione um envelope sonoro percurssivo (env)
example.env = Env.perc()

# Finalmente, adicione-o!
example.add()

# Como criar um SynthDef

with SynthDef("pads") as pads:
    pads.osc = SinOsc.ar(pads.freq)
    pads.env = Env.perc()

# É equivalente a

pads = SynthDef("pads")
pads.osc = SinOsc.ar(pads.freq)
pads.env = Env.perc()
pads.add()
