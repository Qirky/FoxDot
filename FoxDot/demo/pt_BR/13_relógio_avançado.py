# Tutorial 13: Relógio Avançado

# Para ver o que esta agendado para ser tocado.
print(Clock)

# Para ver qual é a latência
print(Clock.latency)

# O relógio pode agendar qualquer objeto que tenha um método __call__, como uma função
# Mas, precisa de um tempo absoluto para agendar a função
# Clock.schedule precisa saber a batida para agendar algo
Clock.schedule()   # lanvata TypeError

# Agende um evento depois de certa duração
# Clock.future precisa saber quantas batidas a frete deve agendar algo
Clock.future()     # lavanta TypeError

# Ambos são equivalentes
Clock.schedule(lambda: print("hello"), Clock.now() + 4)
Clock.future(4, lambda: print("hello"))

# Para agendar alguma coisa
Clock.schedule(lambda: print("hello "))

# Nós podemos chamar algo a cada n batidas
Clock.every(4, lambda: print("hello"))

# Pega o tempo atual e adiciona 2. Útil para agendamentos.
print(Clock.now() + 2)

# Agende para a próxima bara
nextBar(Clock.clear)

# Com um decorador
@nextBar
def change():
    Root.default=4
    Scale.default="minor"
    # etc etc

# Você pode criar suas próprias  e decora-las com isto, para poderem ser
# usadas em um .every de um Player
@PlayerMethod
def test(self):
    print(self.degree)

p1 >> pluck([0,4]).every(3, "test")

# E cancele isso com
p1.never("test")
