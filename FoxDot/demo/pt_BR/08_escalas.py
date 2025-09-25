# Tutorial 8: Escalas


# Por padrão, os Players usam a escala de C Maior.
# Você pode mudar isso usando os parâmetros nomeados: 'scale' e 'root'.
# Escalas podem ser definidas como uma lista de semitons, por exemplo, a escala Maior é [0,2,4,5,7,9,11]
# ou uma escala pré definida no módulo Scale, por exemplo, Scale.minor.
# Root refere-se a tônica da escala; 0 é igual a C, 1 é C#, 2 é D e assim por diante.

# A escala padrão pode ser alterada para todos os player que não use uma escala específica.
# Isso é feito usando a sintaxe abaixo (cada linha é tecnicamente equivalente):

Scale.default.set("major")
Scale.default.set(Scale.major)
Scale.default.set([0,2,4,5,7,9,11])

# Ou a mesma coisa, mas menor:
Scale.default.set("minor")
Scale.default.set(Scale.minor)
Scale.default.set([0,2,3,5,7,10])

# Para econizar tempo, você também pode fazer
Scale.default = "minor"

# O mesmo se aplica para o root:
Root.default.set(1)
Root.default.set("C#")

# Ou:
Root.default.set(2)
Root.default.set("D")

# Para ver a lista de todas as escala, use
print(Scale.names())

# Você pode mudar a escala usada por um player usando o parâmetro 'scale'
p1 >> pads([0,1,2], scale=Scale.minor)

# Similar a escala, você pode mudar a nota raiz do plaeyr usando o parâmetro 'root'
# porem apenas com números, ao contrário do objeto Root.default que aceita string
p1 >> pads([0,1,2], scale=Scale.minor, root=2)
