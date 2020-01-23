import sys
import urllib.request

from functools import reduce

def download(output,wavPath):
	text = reduce(lambda accum,x: accum + x, output, "")
	index = text.find('./temp/') + len('./temp/')
	text = text[index:index+40].split(".")[0]

	urllib.request.urlretrieve("http://sinsy.sp.nitech.ac.jp/temp/" + text + ".wav", wavPath)
