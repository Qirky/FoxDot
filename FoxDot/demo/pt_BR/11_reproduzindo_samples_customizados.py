# Tutorial 11: Reproduzindo Samples Customizados

# Você pode usar seus próprios samples simplismente colocando seus arquivos de áudio dentro do diretório de samples que já existe no FoxDot.
# Ele esta localizado no diretório 'snd' na raiz da instalação do FoxDot
# (por exemplo, 'C:\Python27\Lib\site-packages\FoxDot\snd').

# Você viu anterior mente como tocar samples com o play(). Também é possível tocar sample com o loop().
s1 >> loop('foxdot')

# Você deve ter notado que isso toca apenas a primeira parte do sample repetidamente.
# Esse comportamento poder ser alterado com muitos dos parâmetros que vimos aé agora para controlar outros synths. dur é um bom lugar pra começar
s1 >> loop('foxdot', dur=4)

# Se você tiver um diretório de samples que gostaria de usar com FoxDot, você pode chamar loop() com o caminho completo do sample
s1 >> loop('/path/to/samples/quack.wav')

# Se você passar o caminho de um diretório para o loop, ele irá reproduzir o primeiro sample que encontrar. Você pode mudar o sample que está sendo reproduzido com o parâmetro sample=

# Toque o primeiro sample da minha coleção
s1 >> loop('/path/to/samples')

# Toque o segundo sample da minha coleção
s1 >> loop('/path/to/samples', sample=1)

# Se você for usar muitos sample de um diretório, você pode adiciona-lo aos caminhos usados para buscar os samples. O FoxDot olhará em todos os caminhos para buscar um sample correspondente ao nome.
Samples.addPath('/path/to/samples')
s1 >> loop('quack')

# Depois de ter um caminho de busca, você pode usar a correspondência de padrões para procurar samples.

# Toque o 3 sample dentro do diretório 'snare'
s1 >> loop('snare/*', sample=2)

# Também pode usar * nos nomes dos diretórios
s1 >> loop('*_120bpm/drum*/kick*')

# ** significa "todos os subdiretórios recursivos". Isso reproduzirá o primeiro sample
# aninhado em 'percussion' (por exemplo, 'percussion/kicks/classic/808.wav')
s1 >> loop('percussion/**/*')
