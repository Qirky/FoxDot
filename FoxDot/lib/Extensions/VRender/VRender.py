from __future__ import absolute_import, print_function

import os

from .Constants import *
from .Composer import compose
from .VoiceSpecificator import generateVoiceSpecification
from .Sinsy import download

def renderizeVoice(outputName,lyrics,notes,durations,tempo,scale,sex):

	print("Running voice renderization")

	compose(notes,durations,scale,LAST_MIDI,VOICE_XML_ORIGINAL)

	lyrics = tokenize(lyrics)

	generateVoiceSpecification(lyrics,tempo,VOICE_XML_ORIGINAL,VOICE_XML_PROCESSED)

	urlfileName = os.popen("curl -X POST -F 'SPKR_LANG=english' -F 'SPKR=4' -F 'SYNALPHA=0.55' -F 'VIBPOWER=1' -F 'F0SHIFT=0' -F  'SYNSRC=@" + VOICE_XML_PROCESSED +"' http://sinsy.sp.nitech.ac.jp/index.php | grep 'lf0'").read()
	if sex == "male":
		urlfileName = os.popen("curl -X POST -F 'SPKR_LANG=english' -F 'SPKR=5' -F 'SYNALPHA=0.55' -F 'VIBPOWER=1' -F 'F0SHIFT=0' -F  'SYNSRC=@" + VOICE_XML_PROCESSED +"' http://sinsy.sp.nitech.ac.jp/index.php | grep 'lf0'").read()

	download(urlfileName,LAST_VOICE_WAV)

	os.system("cp " + LAST_VOICE_WAV + " " + WAVS_ROOT + outputName + ".wav")

	print("Finished voice renderization")

def tokenize(text):
	textSyllables = cleanText(text)
	return filter(lambda x: len(x) > 0, textSyllables.replace(" ", "-").split("-"))

def cleanText(text):

	text.replace("\n"," ")
	text = text.lower()

	symbolsToDelete = ".,'!?" + '"'
	for symbol in symbolsToDelete:
		text = text.replace(symbol,"")

	return text
