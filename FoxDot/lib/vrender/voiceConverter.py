# -*- coding: latin-1 -*-
import math
import sys

from utils import *

def cleanText(text):

	text.replace("\n"," ")
	text = text.lower()

	symbolsToDelete = ".,'!?" + '"'
	for symbol in symbolsToDelete:
		text = text.replace(symbol,"")

	return text

def tokenize(text):
	textSyllables = cleanText(text)
	return filter(lambda x: len(x) > 0, textSyllables.replace(" ", "-").split("-"))

def addVoiceTags(tempo, text, content):
	print("El tempo es de:")
	print(tempo)
	print(text)
	output = ""
	tempo_xml = '<direction>\n<sound tempo="{}"/>\n</direction>'.format(tempo)
	lyrics_xml = '<voice>1</voice>\n<lyric>\n<text>{}</text>\n</lyric>'

	i = 0
	ignoreThisNote = False
	for line in content:
		if "<rest/>" in line:
			ignoreThisNote = True
		if "</note" in line:
			if not ignoreThisNote:
				output += lyrics_xml.format(text[i])
				i+=1
			else:
				ignoreThisNote = False

		output += line

		if tempo != -1 and "<measure" in line:
			output += tempo_xml

	return output

def musicGenerator(tempo, text, content):

	text = tokenize(text)
	if len(text) < len(content):
		text = text + (["a"]*int(math.ceil(len(content)/float(len(text)))))[:len(content)]

	return addVoiceTags(tempo, text, content)

def main(lyrics,musicXMLPath, tempo):

	with open(musicXMLPath, 'r') as c:
		content = [x.strip() for x in c.readlines()]
		with open(VOICE_XML_ROOT_PATH+'voice.xml','w') as f:
			f.write(musicGenerator(tempo,lyrics,content))

if __name__ == "__main__":
	try:
		lyrics = sys.argv[1]
		musicXMLPath = sys.argv[2]

		print sys.argv

		if  len(sys.argv) < 4:
			tempo = 80
		else:
			tempo = int(sys.argv[3])

		main(lyrics,musicXMLPath, tempo)
	except:
		print "Invalid Parameters!"
		print "Try something like this:"
		print "\tvoiceAdder.py path/to/lyrics.txt path/to/musicXML.xml 120"
		print "Or this if you want to use the default 80 BPM tempo"
		print "\tvoiceAdder.py path/to/lyrics.txt path/to/musicXML.xml"