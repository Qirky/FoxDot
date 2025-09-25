# Tutorial 3: Reproduzindo Samples Embutidos


# FoxDot também pode usar uma sequência e manipular samples de áudio.
# Para fazer isso, tudo que o você precisa é usar SynthDef especial: o 'play'.
# O primeiro parâmetro do SynthDef play deve ser uma string de caracteres
# diferente de uma lista de números como você faria com outros SynthDef.
# Cara caractere representa um arquico diferente de áudio, que está armazenado em um buffer no SuperCollider.

# Para ver a relação do caracter com cada arquivo de áudio, execute
print(Samples)

# Você pode tocar arquivos de samples nos sub diretórios de FoxDot/snd/ usando o
# Synth 'play' e usand uma string de caracteres ao invés de uma lista de notas.
bd >> play("x")

# Um caractere refere-se a um som e um espaço vazio (ou qualquer outro caractere que não tem uma sample mapeado) é  usado para silencio, então
# você pode espalhar o som pelo tempo
bd >> play("x  x  x  ")

hh >> play(" -")

# Você pode entrelaçar padrões usando parênteses
# isso é equivalente a: "x o  xo "
d1 >> play("(x )( x)o ")

# O código a baixo é o mesmo que "-------="
hh >> play("---(-=)")

# Colocar caracteres entre colchetes tocará tudo em um espaço de uma batida
# e tocará como um caracter, não simultaneamente, mas, em uma rapida subsequência
d1 >> play("x-o[-o]")

d1 >> play("x-o[---]")

d1 >> play("x-o[-----]")

d1 >> play("x-o[--------------]")

# e podem ser colocados entre parênteses como se fosse um único caracter.
d1 >> play("x[--]o(=[-o])")

# Você pode combinar parênteses como desejar: os padrões abaixo são identicos
d1 >> play("x-o(-[-o])")

d1 >> play("x-o[-(o )]")

# As chaves selecionam um sample aleatóriamente, se você quiser mais variação
d1 >> play("x-o{-=[--][-o]}")

# Os colchetes angulares combinam padrões para serem tocados simultaneamente
d1 >> play("<X   ><-   ><#   ><V   >")

d1 >> play("<X   >< -  ><  # ><   V>")

# Cara caracter é mapeado para uma pasta de arquivos se som e você pode selecionar diferentes
# samples usando o parâmetro nomeado "sample"
d1 >> play("(x[--])xu[--]")

d1 >> play("(x[--])xu[--]", sample=1)

d1 >> play("(x[--])xu[--]", sample=2)

# Muda o sample a cada batida
d1 >> play("(x[--])xu[--]", sample=[1,2,3])

# Você pode criar duas camadas de padrões juntos - note o "P", veja o tutorial 4 para mais informações.
d1 >> play(P["x-o-"] & P[" **"])

# E mude efeitos aplicando-o para todas as camadas de padrões ao mesmo tempo
d1 >> play(P["x-o-"] & P[" **"], room=0.5)

# Exemplos com samples para o tutorial de players
# Condicionais...
d1 >> play("x[--]xu[--]x", sample=(d1.degree=="x"))

# Ou mude para o 2 sample multiplicando
d1 >> play("x[--]xu[--]x", sample=(d1.degree=="x")*2)

# Encadeie multiplas condicionais
d1 >> play("x[--]xu[--]x", sample=(d1.degree=="x")*2 + (d1.degree=="-")*5)

# Isso é o mesmo que
d1 >> play("x[--]xu[--]x", sample=d1.degree.map({"x":2, "-":5}))
