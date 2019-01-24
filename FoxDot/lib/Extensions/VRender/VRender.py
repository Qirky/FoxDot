from __future__ import absolute_import, print_function

import os

from .Composer import compose
from .VoiceSpecificator import generateVoiceSpecification
from .Sinsy import download


def renderizeVoice(outputName,lyrics,notes,durations,tempo,scale,sex,local,foxdot_root):

	# Constants
	print(foxdot_root)
	FILES_ROOT = os.path.realpath(foxdot_root + "/lib/Extensions/VRender/tmp/")
	LAST_MIDI = FILES_ROOT + "/last_midi_generated_by_vrender.mid"
	VOICE_XML_ORIGINAL=FILES_ROOT + "/last_voice.musicxml"
	VOICE_XML_PROCESSED=FILES_ROOT+"/last_voice.xml"

	WAVS_ROOT = os.path.realpath(foxdot_root + "/snd/_loop_/")
	LAST_VOICE_WAV = WAVS_ROOT + "/last_voice_generated.wav"


	print("Running voice renderization")

	compose(notes,durations,scale,LAST_MIDI,VOICE_XML_ORIGINAL)

	lyrics = tokenize(lyrics)

	generateVoiceSpecification(lyrics,tempo,VOICE_XML_ORIGINAL,VOICE_XML_PROCESSED)

	if not local:
		if sex == "male":
			urlfileName = os.popen("curl -X POST -F 'SPKR_LANG=english' -F 'SPKR=5' -F 'SYNALPHA=0.55' -F 'VIBPOWER=1' -F 'F0SHIFT=0' -F  'SYNSRC=@" + VOICE_XML_PROCESSED +"' http://sinsy.sp.nitech.ac.jp/index.php | grep 'lf0'").read()
		else:
			urlfileName = os.popen("curl -X POST -F 'SPKR_LANG=english' -F 'SPKR=4' -F 'SYNALPHA=0.55' -F 'VIBPOWER=1' -F 'F0SHIFT=0' -F  'SYNSRC=@" + VOICE_XML_PROCESSED +"' http://sinsy.sp.nitech.ac.jp/index.php | grep 'lf0'").read()

		download(urlfileName,LAST_VOICE_WAV)

	os.system("cp " + LAST_VOICE_WAV + " " + WAVS_ROOT + "/" + outputName + ".wav")

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