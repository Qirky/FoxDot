# Tutorial 5: Atributos Do Player

# Você pode definir uma variável fora o player
pitches = P[0,1,2,3,4]
harmony = pitches + 2

print(pitches)
print(harmony)

p1 >> pluck(pitches)
p2 >> star(harmony)

# Definir a duração diferente para o segundo pode não ter o efeito esperado
p1 >> pluck(pitches)
p2 >> star(harmony, dur=1/2)

# Mas, é possível que um player toque exatamente como um outro player.
# Para que um player siga outro player, use o método follow:
p1 >> pluck(pitches)

p2 >> star(dur=1/2).follow(p1) + 2

# Você também pode referenciar explicitamente um atributo, como o pitch ou a duração:

p2 >> star(p1.pitch) + 2  # isso é o mesmo que .follow(p1)

# Também funciona com outro atributo
p1 >> pluck(pitches)
p2 >> star(dur=p1.dur).follow(p1) + 2

# Você pode referenciar e testar o valor atual
# O == retornará 1 se verdadeira e 0 se falso
print(p1.degree)
print(p1.degree == 2)

# Isso permite que você crie condicionas, como
p1 >> pluck([0,1,2,3], amp=(p1.degree==1))

p1 >> pluck([0,1,2,3], amp=(p1.degree>1))

# Ou mude para um amp diferente multiplicando por 4
p1 >> pluck([0,1,2,3], amp=(p1.degree==1)*4)

# Encadeie multiplas condicionais
p1 >> pluck([0,1,2,3], amp=(p1.degree==1)*4 + (p1.degree==2)*1)

# Que é o mesmo que
p1 >> pluck([0,1,2,3], amp=p1.degree.map({1:4, 2:1}))
