# Tutorial 7: Relógio Básico


# Pare parar o som de todos os player, você pode pressionar Ctrl+.  (Segue Ctrl e bata no ponto)
# Que é um atalho de tecla para o comando:
Clock.clear()

# Mude o tempo (isso tera efeito na próxima barra), o padrão é 120.
Clock.bpm = 144

# Para ver o que esta agendado para ser tocado.
print(Clock)

# Para ver qual é a latência
print(Clock.latency)

# Alguma vezes você quer saber quando que a próxima X batida do ciclo irá começar.
# Para fazer isso nós podemos usar o método 'mod'. Por exemplo, se nós quisermos ver quando
# é o início da próxima 32 batida, podemos fazer
print(Clock.mod(32))

