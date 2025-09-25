# Tutorial 14: Referência dos Atributos Do Player
# --- TODO: this needs updating


# Para ver todos os atributos:
print(Player.get_attributes())

# Você pode ver quais efeitos estão disponíveis executando
print(FxList)

# Vamos usar o filtro passa-alta como exemplo. Você pode isso descrito
# como:
# "<Fx 'highPassFilter' -- args: hpr, hpf>"

# Cada elemento tem um argumento "principal" e então um parametro filho. Aqui o
# argumento principal é "hpf" (abreviação de high pass filter) e o seu argumento filho
# é "hpr" (abreviação de high pass resonance). O efeito é adicionado apenas quando o
# argumento principal for diferente de zero:
d1 >> dirt([0,4,2,1], dur=1/2, hpf=4000)

# Isso define o filtro em 4000 Hz,ou seja, apenas as frequências do sinal
# de áudio *acima* disso serão ouvida. Vamos mudar o valor de ressonância. Seu
# valor padrão é 1, então, vamos diminui-lo
d1 >> dirt([0,4,2,1], dur=1/2, hpf=4000, hpr=0.3)


# Notou uma diferença? Mós podemos usar padrões/var no nósso efeito para criar
# mudanças temporais:
d1 >> dirt([0,4,2,1], dur=1/2, hpf=linvar([0,4000],8), hpr=P[1,1,0.3].stretch(8))




####################
# Referência
####################



####################
# amp - Amplitude (o padrão é 1)
# Define o volume da nota/padrão

d1 >> play("*", dur=1/2, amp=1)

# Metade do Volume
d1 >> play("*", dur=1/2, amp=.5)

# Crie um padrão com amp
d1 >> play("*", dur=1/2, amp=[1,0,1,1,0])



####################
# amplify - Muda o amp, multiplando o valor (em vez de sobrescrever)

# Crie um padrão com amp
d1 >> play("*", dur=1/2, amp=[1,0,1,1,0])
d1 >> play("*", dur=1/2, amplify=[.5,1,0])

# Defnia uma "queda" na música (toca no volume máximo por 28, depois 0 por 4)
p1 >> blip([0,1,2,3], amplify=var([1,0],[28,4]))



####################
# bend



####################
# benddelay - Veja bend



####################
# bits
# A profundidade de bits, em número de bits, à qual o sinal é reduzido;
# deve ser um valor entre 1 e 24, outros valores são ignorados.
# Use crush para definir a quantidade de redução do bitrate (o padrão é 8)



####################
# bitcrush - Veja bits



####################
# blur



####################
# bpf -  Filtro Passa-Faixa



####################
# bpnoise - Veja bpf



####################
# bpr - Veja bpf



####################
# bpm



####################
# buf



####################
# channel



####################
# chop
# 'Corta' o sinal em partes usando pulsos de ondes de baixa frequência durante a sustentação da nota.



####################
# coarse



####################
# comb delay - Veja echo



####################
# crush



####################
# cut
# Fatia a duração
p1 >> pluck(P[:8], dur=1/2, cut=1/8)
p1 >> pluck(P[:8], dur=1/2, cut=1/4)
p1 >> pluck(P[:8], dur=1/2, cut=1/2)



####################
# cutoff



####################
# decay - Veja echo



####################
# degree - Os graus, ou notas, pode ser especificado via parâmetro nomeado (ou o primeiro posicional)
p1 >> blip(degree=[0,1,2,3])

# Que é o mesmo que:
p1 >> blip([0,1,2,3])

# Toca apenas a nota "raiz" do acorde
b1 >> bass(p1.degree[0])



####################
# delay - Uma duração de tempo a ser esperada antes da informação ser enviada ao SuperCollider (o padrão é 0)

# Atrasa toda terceira nota em .1
p1 >> blip([0,1,2,3], delay=[0,0,0.1])

 Atrasa toda terceira nota em .5
p1 >> blip([0,1,2,3], delay=[0,0,0.5])

# Toca a nota para cada delay diferente
p1 >> blip([0,1,2,3], delay=(0,0.1))

p1 >> blip([0,1,2,3], delay=(0,0.25))

p1 >> blip([0,1,2,3], delay=(0,.1,.2,.3))



####################
# dist



####################
# dur - Durações (o padrão é 1 e 1/2 para o 'play()')



####################
# echo
# Principal: echo, Filho: decay
# Define o tempo de decaimento para qualquer efeito de eco em batidas, funciona melhor no 'play()' (o padrão é 0)
# Multiplicando pelo valor da sustentação
d1 >> play("x-o-", echo=0.1)

d1 >> play("x-o-", echo=0.5)

p1 >> pluck(P[:8], echo=.25)

p1 >> pluck(P[:8], echo=.5)

p1 >> pluck(P[:8], echo=.5, decay=.5)



####################
# env



####################
# fmod



####################
# formant



####################
# freq



####################
# hpf - Filtro Passa-Alta
# Filtro as fequências abaixo de um valor, removendo baixas frequências

# 4000 hertz
p1 >> pluck(P[:8], dur=1/2, hpf=4000)

# HPF é 0 por 4 batidas, então, 4000 por 4 batidas
p1 >> pluck(P[:8], dur=1/2, hpf=var([0,4000],[4,4]))

# Mude linearmente o hpf de 0 a 4000 por 4 batidas, 4 batidas voltando para 0
p1 >> pluck(P[:8], dur=1/2, hpf=linvar([0,4000],[4,4]))

# Mude linearmente  o hpf de 0 a 4000 por 8 batidas, então, volte direto para 0
p1 >> pluck(P[:8], dur=1/2, hpf=linvar([0,4000],[8,0]))

# Com uma ressonância diferente (o padrão é 1)
p1 >> pluck(P[:8], dur=1/2, hpf=linvar([0,4000],[8,0]), hpr=.5)

# Com uma ressonância usando um linvar
p1 >> pluck(P[:8], dur=1/2, hpf=linvar([0,4000],[8,0]), hpr=linvar([0.1,1],12))



####################
# hpr - Veja hpf



####################
# lpf - Filtro Passa-Baixa
# Filtro todas as frequências acima de um valor, removendo frequências mais altas

# 4000 hertz
p1 >> pluck(P[:8], dur=1/2, lpf=400)

# Com ressonância mudando com um linvar
p1 >> pluck(P[:8], dur=1/2, lpf=linvar([500,4000],[8,0]), lpr=linvar([0.1,1],12))



####################
# lpr - Veja lpf



####################
# midinote



####################
# pan
# Panorâma, onde -1 é o esquerdo, 1 é o direito (o padrão é 0)



####################
# pitch - Veja degree



####################
# pshift



####################
# oct



####################
# rate
# Parâmetro usado para alterações diversas em um sinal. Por exemplo, taxa de reprodução do 'play()' (o padrão é 1).



####################
# room
# Principal: room, Filho: mix (o padrão é 0.1)

# O parâmetro room especifica o tamanho da sala
d1 >> play("x-o-", room=0.5)

# Mix é a mistura seca/úmida do reverb ou o quanto o reverb é misturado com a fonte. 1 é todo reverb, 0 é nenhum reverb. (0.1 por padrão)
d1 >> play("x-o-", room=0.5, mix=.5)



####################
# Reveb
# Veja Room



####################
# sample
# Parâmetro especial para o 'play()'; seleciona outro arquivo de áudio de um banco de samples de um caracteres.



####################
# scale



####################
# shape



####################
# slide - Deslize para
# Desliza o valor de frequência de um sinal para freq * (slide+1) ao longo da duração de uma nota (o padrão é 0)

p1 >> pluck(P[:8], dur=1/2, slide=1)

p1 >> pluck(P[:8], dur=1/2, slide=12)

p1 >> pluck(P[:8], dur=1/2, slide=var([0,-1],[12,4]))



####################
# slidedelay



####################
# slidefrom



####################
# slider



####################
# spread



####################
# spin



####################
# striate



####################
# stutter



####################
# sus - Sustentação (usa o mesmo valor de `dur` padrão)



####################
# swell



####################
# vib - Vibrato
# Principal: vib, Filho: vibdepth (o padrão é 0.2)

p1 >> pluck(P[:8], dur=1/2, vib=12)

# Com o atributo filho, vibdepth (0.2 por padrão)
p1 >> pluck(P[:8], dur=1/2, vib=12, vibdepth=0.5)



####################
# vibdepth - Veja vib
