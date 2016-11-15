import re
re_player = r"(\w+)\s*?>>\s*?\w+"

re_player = re.compile(re_player)

print re_player.match("bd >> play()").group(1)
